import re
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader

from .source_utils import SourceChunk, chunk_source


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "build" / "data" / "vlearn-pack"

LESSONS = {
    "day1-foundation": {
        "title": "Day 1 - AI & LLM Foundation",
        "slide_file": "d1-slide-hackathon.pdf",
        "transcripts": ["transcript-04-clean.md", "transcript-06-clean.md"],
    },
    "day2-problem": {
        "title": "Day 2 - Xác định bài toán cho AI",
        "slide_file": "d2-slide-hackathon.pdf",
        "transcripts": [
            "transcript-01-clean.md",
            "transcript-02-clean.md",
            "transcript-03-clean.md",
            "transcript-05-clean.md",
        ],
    },
}

WORD = re.compile(r"[\wÀ-ỹ]+", re.UNICODE)
STOPWORDS = {
    "và", "là", "của", "có", "cho", "một", "những", "các", "được", "thì", "mình",
    "bạn", "này", "đó", "với", "trong", "khi", "để", "về", "ra", "ở", "sẽ", "như",
    "the", "a", "an", "to", "of", "and", "is", "are", "in", "for", "on",
}


def get_lesson(lesson_id: str) -> dict:
    lesson = LESSONS.get(lesson_id)
    if not lesson:
        raise ValueError("Bài học không tồn tại.")
    return lesson


def get_slide_path(lesson_id: str) -> Path:
    lesson = get_lesson(lesson_id)
    path = DATA_ROOT / "slides" / lesson["slide_file"]
    if not path.is_file():
        raise ValueError("Không tìm thấy file slide của bài học.")
    return path


@lru_cache(maxsize=4)
def get_pdf_reader(lesson_id: str) -> PdfReader:
    return PdfReader(str(get_slide_path(lesson_id)))


def lesson_catalog() -> list[dict]:
    catalog = []
    for lesson_id, lesson in LESSONS.items():
        catalog.append(
            {
                "id": lesson_id,
                "title": lesson["title"],
                "slide_count": len(get_pdf_reader(lesson_id).pages),
                "slide_url": f"/data/slides/{lesson_id}.pdf",
                "transcript_count": len(lesson["transcripts"]),
            }
        )
    return catalog


@lru_cache(maxsize=4)
def transcript_chunks(lesson_id: str) -> tuple[SourceChunk, ...]:
    lesson = get_lesson(lesson_id)
    chunks: list[SourceChunk] = []
    for filename in lesson["transcripts"]:
        path = DATA_ROOT / "transcript" / filename
        chunks.extend(chunk_source(path.read_text(encoding="utf-8"), "transcript"))
    return tuple(chunks)


def _terms(text: str) -> set[str]:
    return {word.casefold() for word in WORD.findall(text) if len(word) > 2 and word.casefold() not in STOPWORDS}


def _score(query_terms: set[str], chunk: SourceChunk) -> float:
    chunk_terms = _terms(chunk.text)
    if not query_terms or not chunk_terms:
        return 0.0
    overlap = query_terms & chunk_terms
    return len(overlap) / max(len(query_terms), 1) + len(overlap) / max(len(chunk_terms), 1)


def review_context(lesson_id: str, slide_number: int, notes: str, transcript_limit: int = 8) -> list[SourceChunk]:
    reader = get_pdf_reader(lesson_id)
    if slide_number < 1 or slide_number > len(reader.pages):
        raise ValueError(f"Slide phải nằm trong khoảng 1-{len(reader.pages)}.")

    slide_text = (reader.pages[slide_number - 1].extract_text() or "").strip()
    if not slide_text:
        raise ValueError("Slide hiện tại không có text để đối chiếu. Hãy chọn slide khác.")

    slide_chunk = SourceChunk("slide", f"Slide {slide_number}", slide_text)
    query_terms = _terms(f"{slide_text}\n{notes}")
    ranked = sorted(transcript_chunks(lesson_id), key=lambda item: _score(query_terms, item), reverse=True)
    related = [chunk for chunk in ranked if len(chunk.text) >= 50 and _score(query_terms, chunk) > 0][:transcript_limit]
    return [slide_chunk, *related]
