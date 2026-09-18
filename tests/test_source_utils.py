from codebase.schemas import Finding
from codebase.source_utils import chunk_source, validate_and_ground


SOURCE = """**[T03-N001]** Token là đơn vị văn bản mà mô hình xử lý.

**[T03-N002]** Context window có giới hạn và phụ thuộc vào model."""


def test_chunks_preserve_transcript_ids():
    chunks = chunk_source(SOURCE, "transcript")
    assert [chunk.source_id for chunk in chunks] == ["T03-N001", "T03-N002"]


def test_invalid_citation_downgrades_claim():
    finding = Finding.model_validate(
        {
            "status": "misconception",
            "note_excerpt": "Token luôn là một từ.",
            "finding": "Nhận định mâu thuẫn với nguồn.",
            "explanation": "Nguồn định nghĩa token khác.",
            "citations": [{"source_type": "transcript", "source_id": "T03-N001", "quote": "Một câu bịa đặt"}],
            "suggested_revision": "Token là đơn vị văn bản mà mô hình xử lý.",
            "review_question": "Token có luôn trùng với một từ không?",
            "confidence": "high",
        }
    )
    [validated] = validate_and_ground([finding], chunk_source(SOURCE, "transcript"))
    assert validated.status.value == "insufficient_evidence"
    assert validated.citations == []
    assert validated.suggested_revision == ""

