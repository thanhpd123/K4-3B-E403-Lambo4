from codebase.app import app
from codebase.lesson_data import review_context
from codebase.study_flow import _ground, _plans, _attempts
from codebase.source_utils import SourceChunk
from codebase.study_flow import Signal


def test_unmatched_source_downgrades_signal():
    signal = Signal(
        concept="Tokenization", status="misconception", evidence_excerpt="Token luôn là một từ.",
        reason="Sai với nguồn", source_type="transcript", source_id="T01-N001",
        source_quote="Câu không có trong nguồn", question="Token có luôn là một từ không?",
        expected_answer="Không", grading_criteria="Nêu được ngoại lệ",
    )
    result = _ground(signal, [SourceChunk("transcript", "T01-N001", "Token có thể là mảnh của từ.")], "Token luôn là một từ.", "")
    assert result.status == "insufficient_evidence"
    assert result.question == ""


def test_question_alone_cannot_be_misconception():
    source = SourceChunk("transcript", "T01-N001", "Token có thể là một phần của từ.")
    signal = Signal(
        concept="Tokenization", status="misconception", evidence_excerpt="Token có luôn là một từ?",
        reason="Model đoán hiểu sai", source_type="transcript", source_id="T01-N001",
        source_quote="Token có thể là một phần của từ.",
        question="Token có luôn tương ứng với một từ không?",
        expected_answer="Không", grading_criteria="Nêu được ví dụ token là một phần của từ.",
    )
    result = _ground(signal, [source], "Ghi chú về token.", "Token có luôn là một từ?")
    assert result.status == "insufficient_evidence"


def test_uncertain_signal_can_have_no_source():
    signal = Signal(concept="Chủ đề ngoài bài", status="insufficient_evidence", reason="Nguồn không đề cập.")
    result = _ground(signal, [], "Ghi chú ngoài bài.", "")
    assert result.status == "insufficient_evidence"
    assert result.source_id == ""


def test_mock_flow_requires_approval_and_reports_attempt(monkeypatch):
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "true")
    _plans.clear()
    _attempts.clear()
    client = app.test_client()
    analysis = client.post("/api/study/analyze", json={
        "lesson_id": "day1-foundation", "slide_number": 4,
        "notes": "Token là đơn vị văn bản.", "chat": "Token có phải luôn là một từ?",
    })
    assert analysis.status_code == 200
    data = analysis.json
    assert data["is_mock"] is True
    assert data["signals"][0]["status"] == "unnoted"
    plan_id = data["plan_id"]
    answer = {"answers": [{"signal_id": "1", "text": "Câu trả lời của tôi."}]}
    assert client.post(f"/api/study/{plan_id}/submit", json=answer).status_code == 400
    approved = client.post(f"/api/study/{plan_id}/approve", json={"questions": [{
        "signal_id": "1", "question": "Bạn giải thích ý chính của trang này như thế nào?",
        "expected_answer": "Theo nguồn của slide.", "grading_criteria": "Có ý chính và lý do.",
    }]})
    assert approved.status_code == 200
    assert "expected_answer" not in approved.json["questions"][0]
    result = client.post(f"/api/study/{plan_id}/submit", json=answer)
    assert result.status_code == 200
    assert result.json["outcomes"][0]["verdict"] == "uncertain"
    report = client.get("/api/study/report/day1-foundation").json
    assert report["attempts"] == 0
    assert report["mock_attempts"] == 1
    assert report["concepts"] == []


def test_real_analysis_grounds_claim_and_rejects_unsupported_quiz(monkeypatch):
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "false")
    _plans.clear()
    chunks = review_context("day1-foundation", 4, "Token là đơn vị văn bản.")
    source = chunks[0]
    monkeypatch.setattr("codebase.study_flow.generate_json", lambda *_: ({"signals": [{
        "concept": "Tokenization", "status": "misconception",
        "evidence_excerpt": "Token luôn là một từ.", "reason": "Sai với nguồn",
        "source_type": source.source_type, "source_id": source.source_id,
        "source_quote": "Trích dẫn bịa", "question": "Token luôn là một từ không?",
        "expected_answer": "Không", "grading_criteria": "Giải thích được",
    }]}, "fake-provider"))
    result = app.test_client().post("/api/study/analyze", json={
        "lesson_id": "day1-foundation", "slide_number": 4,
        "notes": "Token luôn là một từ.", "chat": "",
    })
    assert result.status_code == 200
    assert result.json["signals"][0]["status"] == "insufficient_evidence"
    plan_id = result.json["plan_id"]
    rejected = app.test_client().post(f"/api/study/{plan_id}/approve", json={"questions": [{
        "signal_id": "1", "question": "Token có luôn tương ứng với một từ không?",
        "expected_answer": "Không", "grading_criteria": "Nêu được lý do",
    }]})
    assert rejected.status_code == 400


def test_grounded_real_flow_uses_ai_grading_and_aggregates(monkeypatch):
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "false")
    _plans.clear()
    _attempts.clear()
    slide = review_context("day1-foundation", 4, "LLM tạo nội dung")[0]
    quote = slide.text[:80].strip()
    calls = []

    def fake_generate(system, prompt):
        calls.append(system)
        if len(calls) == 1:
            return {"signals": [{
                "concept": "Nội dung slide 4", "status": "unnoted", "evidence_excerpt": "",
                "reason": "Ý này cần được kiểm tra bằng quiz.", "source_type": "slide",
                "source_id": "Slide 4", "source_quote": quote,
                "question": "Hãy giải thích ý chính của slide 4 bằng lời của bạn?",
                "expected_answer": "Nêu đúng nội dung slide.",
                "grading_criteria": "Có ý chính và lý do phù hợp nguồn.",
            }]}, "fake-provider"
        return {"grades": [{"signal_id": "1", "verdict": "needs_review", "feedback": "Thiếu ý chính của slide."}]}, "fake-provider"

    monkeypatch.setattr("codebase.study_flow.generate_json", fake_generate)
    client = app.test_client()
    analysis = client.post("/api/study/analyze", json={
        "lesson_id": "day1-foundation", "slide_number": 4,
        "notes": "Tôi ghi một ý khác.", "chat": "",
    })
    assert analysis.status_code == 200
    assert analysis.json["signals"][0]["status"] == "unnoted"
    plan_id = analysis.json["plan_id"]
    approval = client.post(f"/api/study/{plan_id}/approve", json={"questions": [{
        "signal_id": "1", "question": "Hãy giải thích ý chính của slide 4 bằng lời của bạn?",
        "expected_answer": "Nêu đúng nội dung slide.",
        "grading_criteria": "Có ý chính và lý do phù hợp nguồn.",
    }]})
    assert approval.status_code == 200
    submission = client.post(f"/api/study/{plan_id}/submit", json={
        "answers": [{"signal_id": "1", "text": "Tôi chưa nhớ rõ."}]
    })
    assert submission.status_code == 200
    assert submission.json["outcomes"][0]["verdict"] == "needs_review"
    assert client.get("/api/study/report/day1-foundation").json["concepts"][0]["needs_review"] == 1
    assert len(calls) == 2


def test_no_issue_does_not_invent_quiz(monkeypatch):
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "false")
    monkeypatch.setattr("codebase.study_flow.generate_json", lambda *_: ({"signals": []}, "fake-provider"))
    response = app.test_client().post("/api/study/analyze", json={
        "lesson_id": "day1-foundation", "slide_number": 4,
        "notes": "Tôi đã ghi đủ ý trong slide.", "chat": "",
    })
    assert response.status_code == 200
    assert response.json["signals"] == []
