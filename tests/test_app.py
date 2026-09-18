from codebase.app import app


def test_health_reports_missing_provider(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("NOTE_REVIEWER_MOCK", raising=False)

    response = app.test_client().get("/api/health")
    assert response.status_code == 200
    assert response.json["provider"] == "none"


def test_review_requires_key_when_mock_is_off(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "false")

    response = app.test_client().post(
        "/api/review",
        data={
            "notes": "Token là đơn vị văn bản.",
            "source_text": "[T01-N001] Token là đơn vị văn bản mà mô hình xử lý.",
            "source_type": "transcript",
        },
    )
    assert response.status_code == 400
    assert "API key" in response.json["error"]


def test_explicit_mock_returns_labeled_response(monkeypatch):
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "true")

    response = app.test_client().post(
        "/api/review",
        data={
            "notes": "Token là đơn vị văn bản.",
            "source_text": "[T01-N001] Token là đơn vị văn bản mà mô hình xử lý.",
            "source_type": "transcript",
        },
    )
    assert response.status_code == 200
    assert response.json["is_mock"] is True
    assert response.json["provider"] == "mock"
