"""Chạy trọn bộ golden set qua AI thật và ghi kết quả vào results_round_1.json.

Cách dùng:
    python eval/run_eval.py

Yêu cầu: file .env có GEMINI_API_KEY hoặc OPENAI_API_KEY, và NOTE_REVIEWER_MOCK=false.
Kết quả ghi đè eval/results_round_1.json (status, provider, model, run_at, summary, cases).
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from codebase.ai_client import review_notes
from codebase.source_utils import chunk_source, validate_and_ground

load_dotenv(ROOT / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("eval")

GOLDEN = ROOT / "eval" / "golden_set.json"

QUALITY_BAR = {
    "minimum_case_pass_rate": 0.8,
    "citation_validity": 1.0,
    "fabricated_citations_allowed": 0,
}


def _provider_model() -> str:
    if os.getenv("GEMINI_API_KEY"):
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def evaluate_case(case: dict) -> dict:
    chunks = chunk_source(case["source"], case["source_type"])
    result = review_notes(case["notes"], chunks)
    raw_findings = result.response.findings
    raw_citations = sum(len(f.citations) for f in raw_findings)
    grounded = validate_and_ground(raw_findings, chunks)
    grounded_citations = sum(len(f.citations) for f in grounded)

    expected = case["expected_status"]
    matched = next((f for f in grounded if f.status.value == expected), None)
    citation_ok = True
    if case.get("citation_required"):
        citation_ok = bool(matched and matched.citations)
    passed = bool(matched and citation_ok)

    return {
        "id": case["id"],
        "category": case.get("category", ""),
        "passed": passed,
        "expected_status": expected,
        "returned_statuses": [f.status.value for f in grounded],
        "citation_ok": citation_ok,
        "valid_citations": grounded_citations,
        "fabricated_citations": raw_citations - grounded_citations,
        "provider": result.provider,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Chạy golden set qua AI thật.")
    parser.add_argument("--round", type=int, default=1, help="Số thứ tự lượt chạy (ghi results_round_N.json).")
    args = parser.parse_args()
    results_path = ROOT / "eval" / f"results_round_{args.round}.json"

    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    cases = data["cases"]

    results_cases = []
    passed = 0
    fabricated_total = 0
    valid_total = 0
    provider = None
    model = _provider_model()

    for case in cases:
        try:
            r = evaluate_case(case)
        except Exception as exc:  # noqa: BLE001 - ghi nhận case fail để bảng kết quả đủ mọi case
            logger.exception("case %s failed", case["id"])
            r = {
                "id": case["id"],
                "category": case.get("category", ""),
                "passed": False,
                "expected_status": case.get("expected_status"),
                "returned_statuses": [],
                "citation_ok": False,
                "fabricated_citations": 0,
                "provider": None,
                "error": str(exc),
            }
        if r.get("passed"):
            passed += 1
        fabricated_total += r.get("fabricated_citations", 0)
        valid_total += r.get("valid_citations", 0)
        provider = r.get("provider") or provider
        results_cases.append(r)
        logger.info(
            "case=%s passed=%s expected=%s statuses=%s fabricated=%s",
            r["id"],
            r.get("passed"),
            r.get("expected_status"),
            r.get("returned_statuses"),
            r.get("fabricated_citations"),
        )

    total = len(cases)
    pass_rate = round(passed / total, 4) if total else None
    output = {
        "round": args.round,
        "status": "completed",
        "provider": provider,
        "model": model,
        "run_at": datetime.now(timezone.utc).isoformat(),
        "quality_bar": QUALITY_BAR,
        "summary": {
            "passed": passed,
            "total": total,
            "pass_rate": pass_rate,
            "valid_citations": valid_total,
            "fabricated_citations": fabricated_total,
        },
        "cases": results_cases,
    }
    results_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(
        "done passed=%d/%d pass_rate=%s fabricated_citations=%d",
        passed,
        total,
        pass_rate,
        fabricated_total,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
