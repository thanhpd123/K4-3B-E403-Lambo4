import io
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pydantic import ValidationError
from pypdf import PdfReader

from .ai_client import AIConfigurationError, AIResponseError, review_notes
from .mock_ai import mock_review
from .schemas import ReviewRequest
from .source_utils import chunk_source, validate_and_ground

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def _bool_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _extract_upload(file) -> str:
    content = file.read()
    if file.filename and file.filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n\n".join(f"Slide {i}\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages, 1))
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File văn bản phải dùng mã hóa UTF-8.") from exc


@app.get("/")
def index():
    has_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY"))
    return render_template("index.html", has_key=has_key, mock_mode=_bool_env("NOTE_REVIEWER_MOCK"))


@app.post("/api/review")
def api_review():
    try:
        source_text = request.form.get("source_text", "").strip()
        uploaded = request.files.get("source_file")
        if uploaded and uploaded.filename:
            source_text = _extract_upload(uploaded)
        payload = ReviewRequest.model_validate(
            {
                "notes": request.form.get("notes", "").strip(),
                "source_text": source_text,
                "source_type": request.form.get("source_type", "transcript"),
            }
        )
        chunks = chunk_source(payload.source_text, payload.source_type)
        if not chunks:
            return jsonify(error="Không tách được nội dung nguồn. Hãy chọn file hoặc dán nguồn khác."), 400

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

