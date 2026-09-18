import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file
from pydantic import ValidationError

from .ai_client import AIConfigurationError, AIResponseError, review_notes
from .lesson_data import get_slide_path, lesson_catalog, review_context
from .mock_ai import mock_review
from .schemas import ReviewRequest
from .source_utils import validate_and_ground

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def _bool_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


@app.get("/")
def index():
    has_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY"))
    return render_template(
        "index.html",
        has_key=has_key,
        mock_mode=_bool_env("NOTE_REVIEWER_MOCK"),
        lessons=lesson_catalog(),
    )


@app.get("/api/lessons")
def api_lessons():
    return jsonify(lessons=lesson_catalog())


@app.get("/data/slides/<lesson_id>.pdf")
def lesson_slides(lesson_id: str):
    try:
        return send_file(get_slide_path(lesson_id), mimetype="application/pdf", conditional=True)
    except ValueError as exc:
        return jsonify(error=str(exc)), 404


@app.post("/api/review")
def api_review():
    try:
        payload = ReviewRequest.model_validate(
            {
                "notes": request.form.get("notes", "").strip(),
                "lesson_id": request.form.get("lesson_id", "").strip(),
                "slide_number": request.form.get("slide_number", ""),
            }
        )
        chunks = review_context(payload.lesson_id, payload.slide_number, payload.notes)
        if not chunks:
            return jsonify(error="Không tìm được nguồn phù hợp cho slide hiện tại."), 400

        if _bool_env("NOTE_REVIEWER_MOCK"):
            response = mock_review(payload.notes, chunks)
            provider = "mock"
        else:
            result = review_notes(payload.notes, chunks)
            response, provider = result.response, result.provider

        response.findings = validate_and_ground(response.findings, chunks)
        response.provider = provider
        logger.info("Review completed provider=%s findings=%d", provider, len(response.findings))
        return jsonify(response.model_dump(mode="json"))
    except ValidationError as exc:
        return jsonify(error="Ghi chú hoặc nguồn chưa đủ nội dung.", details=exc.errors(include_url=False)), 400
    except (ValueError, AIConfigurationError) as exc:
        return jsonify(error=str(exc)), 400
    except AIResponseError as exc:
        return jsonify(error=str(exc)), 502
    except Exception:
        logger.exception("Review request failed")
        return jsonify(error="Không thể gọi dịch vụ AI lúc này. Kiểm tra API key, kết nối và thử lại."), 502


@app.get("/api/health")
def health():
    provider = "gemini" if os.getenv("GEMINI_API_KEY") else "openai" if os.getenv("OPENAI_API_KEY") else "none"
    return jsonify(status="ok", provider=provider, mock_mode=_bool_env("NOTE_REVIEWER_MOCK"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=_bool_env("FLASK_DEBUG"))
