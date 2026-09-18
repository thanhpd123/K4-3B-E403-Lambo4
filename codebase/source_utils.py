import re
import unicodedata
from dataclasses import dataclass

from .schemas import Citation, Finding, ReviewStatus


@dataclass(frozen=True)
class SourceChunk:
    source_type: str
    source_id: str
    text: str


TRANSCRIPT_ID = re.compile(r"\[(T\d{2}-(?:N)?\d{3})\]")
SLIDE_ID = re.compile(r"(?:^|\n)\s*(?:#{1,3}\s*)?Slide\s+(\d+)\b", re.IGNORECASE)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def chunk_source(source_text: str, source_type: str) -> list[SourceChunk]:
    if source_type == "transcript":
        matches = list(TRANSCRIPT_ID.finditer(source_text))
        if matches:
            return [
                SourceChunk("transcript", match.group(1), source_text[match.end() : matches[i + 1].start() if i + 1 < len(matches) else len(source_text)].strip())
                for i, match in enumerate(matches)
                if source_text[match.end() : matches[i + 1].start() if i + 1 < len(matches) else len(source_text)].strip()
            ]
    else:
        matches = list(SLIDE_ID.finditer(source_text))
        if matches:
            return [
                SourceChunk("slide", f"Slide {match.group(1)}", source_text[match.end() : matches[i + 1].start() if i + 1 < len(matches) else len(source_text)].strip())
                for i, match in enumerate(matches)
            ]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", source_text) if p.strip()]
    prefix = "Slide" if source_type == "slide" else "SRC-N"
    return [
        SourceChunk(source_type, f"{prefix} {i}" if source_type == "slide" else f"{prefix}{i:03d}", paragraph)
        for i, paragraph in enumerate(paragraphs, start=1)
    ]


def validate_and_ground(findings: list[Finding], chunks: list[SourceChunk]) -> list[Finding]:
    by_id = {chunk.source_id: chunk for chunk in chunks}
    grounded: list[Finding] = []
    for finding in findings:
        valid: list[Citation] = []
        for citation in finding.citations:
            chunk = by_id.get(citation.source_id)
            if chunk and citation.source_type == chunk.source_type and normalize(citation.quote) in normalize(chunk.text):
                valid.append(citation)

        finding.citations = valid
        if finding.status in {ReviewStatus.misconception, ReviewStatus.missing_boundary} and not valid:
            finding.status = ReviewStatus.insufficient_evidence
            finding.finding = "Không đủ căn cứ để xác nhận nhận định ban đầu."
            finding.explanation = "Citation do AI cung cấp không khớp chính xác với nguồn đã chọn, nên hệ thống không kết luận ghi chú sai hoặc thiếu."
            finding.suggested_revision = ""
            finding.confidence = "low"
        grounded.append(finding)
    return grounded
