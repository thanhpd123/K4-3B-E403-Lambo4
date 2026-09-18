import json
import logging
import os
import re
from dataclasses import dataclass

from pydantic import ValidationError

from .prompt import SYSTEM_PROMPT, build_user_prompt
from .schemas import AIReviewPayload, ReviewResponse
from .source_utils import SourceChunk

logger = logging.getLogger(__name__)


class AIConfigurationError(RuntimeError):
    pass


class AIResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class AIResult:
    response: ReviewResponse
    provider: str


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else text


def _parse(text: str) -> ReviewResponse:
    try:
        payload = json.loads(_strip_json_fence(text))
        return ReviewResponse.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("Invalid model response: type=%s chars=%s", type(exc).__name__, len(text))
        raise AIResponseError("AI trả về dữ liệu không đúng cấu trúc an toàn. Vui lòng thử lại.") from exc


def _formatted_source(chunks: list[SourceChunk]) -> str:
    return "\n\n".join(f"[{c.source_type} | {c.source_id}]\n{c.text}" for c in chunks)


def _call_gemini(prompt: str) -> ReviewResponse:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return _parse(result.text or "")


def _call_openai(prompt: str) -> ReviewResponse:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=SYSTEM_PROMPT,
        input=prompt,
        temperature=0.1,
        text={
            "format": {
                "type": "json_schema",
                "name": "note_review",
                "schema": AIReviewPayload.model_json_schema(),
                "strict": True,
            }
        },
    )
    return _parse(result.output_text)


def review_notes(notes: str, chunks: list[SourceChunk]) -> AIResult:
    prompt = build_user_prompt(notes, _formatted_source(chunks))
    if os.getenv("GEMINI_API_KEY"):
        logger.info("Review request provider=gemini note_chars=%d source_chunks=%d", len(notes), len(chunks))
        return AIResult(_call_gemini(prompt), "gemini")
    if os.getenv("OPENAI_API_KEY"):
        logger.info("Review request provider=openai note_chars=%d source_chunks=%d", len(notes), len(chunks))
        return AIResult(_call_openai(prompt), "openai")
    raise AIConfigurationError(
        "Chưa cấu hình API key. Hãy tạo file .env từ .env.example và điền GEMINI_API_KEY hoặc OPENAI_API_KEY."
    )
