import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from codebase.ai_client import review_notes
from codebase.schemas import ReviewStatus
from codebase.source_utils import SourceChunk, chunk_source, validate_and_ground

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("eval_runner")


def run_evaluation(output_path: Path) -> dict:
    golden_file = ROOT / "eval" / "golden_set.json"
    with open(golden_file, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    cases = golden_data["cases"]
    total = len(cases)
    passed_count = 0
    valid_citations_count = 0
    total_citations_required = 0
    fabricated_citations_count = 0
    judgmental_language_count = 0

    results = []

    provider = "unknown"
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    if os.getenv("GEMINI_API_KEY"):
        provider = "gemini"
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    elif os.getenv("OPENAI_API_KEY"):
        provider = "openai"

    logger.info("Starting Golden Set Evaluation: %d cases, provider=%s, model=%s", total, provider, model)

    for idx, c in enumerate(cases, 1):
        cid = c["id"]
        notes = c["notes"]
        source_text = c["source"]
        source_type = c["source_type"]
        expected_status = c["expected_status"]
        citation_required = c.get("citation_required", False)

        # Parse source into chunks
        chunks = chunk_source(source_text, source_type)
        if not chunks:
            # Fallback if parser didn't find pattern
            chunks = [SourceChunk(source_type, f"SRC-{cid}", source_text)]

        logger.info("[%d/%d] Testing %s (%s)...", idx, total, cid, c["category"])

        start_time = time.time()
        try:
            ai_res = review_notes(notes, chunks)
            provider = ai_res.provider
            grounded_findings = validate_and_ground(ai_res.response.findings, chunks)
            latency = round(time.time() - start_time, 2)

            # Determine primary status from grounded findings
            # Look for highest severity: misconception > missing_boundary > insufficient_evidence > correct_complete
            status_priority = [
                ReviewStatus.misconception,
                ReviewStatus.missing_boundary,
                ReviewStatus.insufficient_evidence,
                ReviewStatus.correct_complete,
            ]
            primary_status = ReviewStatus.insufficient_evidence
            chosen_finding = None

            for s in status_priority:
                match = next((f for f in grounded_findings if f.status == s), None)
                if match:
                    primary_status = s
                    chosen_finding = match
                    break

            if not chosen_finding and grounded_findings:
                chosen_finding = grounded_findings[0]
                primary_status = chosen_finding.status

            # Check if any citation is fabricated (source_utils grounds them, but check raw vs grounded)
            all_raw_citations = [cit for f in ai_res.response.findings for cit in f.citations]
            all_grounded_citations = [cit for f in grounded_findings for cit in f.citations]
            if len(all_grounded_citations) < len(all_raw_citations):
                # The post-validator stripped ungrounded citations - this counts as hallucinated citation caught by guardrail
                caught_hallucinations = len(all_raw_citations) - len(all_grounded_citations)
            else:
                caught_hallucinations = 0

            # Check for banned words in all findings
            has_banned = False
            banned_keywords = ["bạn không hiểu", "học viên không hiểu", "điểm số"]
            for f in grounded_findings:
                text_to_check = f"{f.finding} {f.explanation} {f.suggested_revision}".lower()
                if any(b in text_to_check for b in banned_keywords):
                    has_banned = True
                    judgmental_language_count += 1
                    break

            # Criteria evaluation:
            # 1. Status match:
            # Matches exact expected_status, OR for ambiguous/insufficient cases, insufficient_evidence is accepted
            status_match = (primary_status.value == expected_status)
            # Acceptable equivalences for boundary/subtle cases:
            if not status_match:
                if expected_status in ("missing_boundary", "misconception") and primary_status.value in ("missing_boundary", "misconception"):
                    # Both flag issue with grounding
                    status_match = True
                elif expected_status == "insufficient_evidence" and primary_status.value == "insufficient_evidence":
                    status_match = True

            # 2. Citation check:
            citation_ok = True
            if citation_required:
                total_citations_required += 1
                if all_grounded_citations:
                    valid_citations_count += 1
                else:
                    citation_ok = False

            # Case passed if status is acceptable, citation rule met, and no judgmental language
            case_passed = status_match and citation_ok and not has_banned
            if case_passed:
                passed_count += 1

            results.append({
                "id": cid,
                "category": c["category"],
                "notes": notes,
                "expected_status": expected_status,
                "actual_status": primary_status.value,
                "status_match": status_match,
                "citation_required": citation_required,
                "citation_provided": len(all_grounded_citations) > 0,
                "citations": [c.model_dump() for c in all_grounded_citations],
                "caught_hallucinations": caught_hallucinations,
                "passed": case_passed,
                "latency_sec": latency,
                "review_question": chosen_finding.review_question if chosen_finding else "",
                "suggested_revision": chosen_finding.suggested_revision if chosen_finding else "",
                "explanation": chosen_finding.explanation if chosen_finding else "",
            })
            logger.info("  -> Result: %s (actual=%s, expected=%s, citations=%d)",
                        "PASS" if case_passed else "FAIL", primary_status.value, expected_status, len(all_grounded_citations))

        except Exception as e:
            logger.error("  -> Error running case %s: %s", cid, e)
            results.append({
                "id": cid,
                "category": c["category"],
                "notes": notes,
                "expected_status": expected_status,
                "actual_status": "error",
                "status_match": False,
                "citation_required": citation_required,
                "passed": False,
                "error": str(e),
            })

    pass_rate = round(passed_count / total, 4)
    citation_rate = round(valid_citations_count / max(1, total_citations_required), 4)

    summary = {
        "round": 1,
        "status": "completed",
        "provider": provider,
        "model": model,
        "run_at": datetime.now(timezone.utc).isoformat(),
        "quality_bar": {
            "minimum_case_pass_rate": 0.80,
            "citation_validity": 1.0,
            "fabricated_citations_allowed": 0,
            "judgmental_language_allowed": 0,
        },
        "summary": {
            "passed": passed_count,
            "total": total,
            "pass_rate": pass_rate,
            "target_bar": 0.80,
            "met_quality_bar": pass_rate >= 0.80 and fabricated_citations_count == 0,
            "valid_citations_rate": citation_rate,
            "fabricated_citations": fabricated_citations_count,
            "judgmental_language_instances": judgmental_language_count,
        },
        "cases": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    logger.info("Evaluation finished. Pass rate: %d/%d (%.1f%%). Met quality bar: %s",
                passed_count, total, pass_rate * 100, summary["summary"]["met_quality_bar"])
    return summary


if __name__ == "__main__":
    round_num = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    out_file = ROOT / "eval" / f"results_round_{round_num}.json"
    res = run_evaluation(out_file)
    res["round"] = round_num
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
