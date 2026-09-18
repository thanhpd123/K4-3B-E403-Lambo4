from codebase.app import app


def test_health_reports_missing_provider(monkeypatch):
    from codebase.app import app

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("NOTE_REVIEWER_MOCK", raising=False)

    response = app.test_client().get("/api/health")
    assert response.status_code == 200
    assert response.json["provider"] == "none"


def test_review_requires_key_when_mock_is_off(monkeypatch):
    from codebase.app import app

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("NOTE_REVIEWER_MOCK", "false")

    response = app.test_client().post(
        "/api/review",
        data={
            "notes": "Token là đơn vị văn bản.",
            "lesson_id": "day1-foundation",
            "slide_number": "4",
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
            "lesson_id": "day1-foundation",
            "slide_number": "4",
        },
    )
    assert response.status_code == 200
    assert response.json["is_mock"] is True
    assert response.json["provider"] == "mock"


def test_lessons_and_slide_pdf_are_served():
    from codebase.app import app

    client = app.test_client()
    catalog = client.get("/api/lessons")
    pdf = client.get("/data/slides/day1-foundation.pdf")
    assert catalog.status_code == 200
    assert len(catalog.json["lessons"]) == 2
    assert catalog.json["lessons"][0]["slide_count"] == 29
    assert pdf.status_code == 200
    assert pdf.content_type == "application/pdf"
