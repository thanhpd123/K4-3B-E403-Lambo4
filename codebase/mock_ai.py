"""Explicit UI-test mock. Enabled only with NOTE_REVIEWER_MOCK=true."""

from .schemas import ReviewResponse
from .source_utils import SourceChunk


def mock_review(notes: str, chunks: list[SourceChunk]) -> ReviewResponse:
    chunk = chunks[0]
    quote = chunk.text[: min(180, len(chunk.text))].strip()
    return ReviewResponse.model_validate(
        {
            "findings": [
                {
                    "status": "correct_complete",
                    "note_excerpt": notes[: min(180, len(notes))],
                    "finding": "Mock UI: ghi chú đã được đưa qua luồng hiển thị.",
                    "explanation": "Đây là kết quả giả lập để kiểm thử giao diện, không phải đánh giá của AI.",
                    "citations": [{"source_type": chunk.source_type, "source_id": chunk.source_id, "quote": quote}],
                    "suggested_revision": "",
                    "review_question": "Bạn có thể giải thích lại ý này bằng lời của mình không?",
                    "confidence": "low",
                }
            ],
            "provider": "mock",
            "is_mock": True,
        }
    )

