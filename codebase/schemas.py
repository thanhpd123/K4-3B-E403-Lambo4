from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ReviewStatus(str, Enum):
    correct_complete = "correct_complete"
    misconception = "misconception"
    missing_boundary = "missing_boundary"
    missing_concept = "missing_concept"
    insufficient_evidence = "insufficient_evidence"


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: str = Field(pattern=r"^(transcript|slide)$")
    source_id: str = Field(min_length=1, max_length=80)
    quote: str = Field(min_length=1, max_length=1000)


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ReviewStatus
    note_excerpt: str = Field(max_length=1500)
    finding: str = Field(min_length=1, max_length=1500)
    explanation: str = Field(min_length=1, max_length=2500)
    citations: list[Citation] = Field(max_length=5)
    suggested_revision: str = Field(max_length=2500)
    review_question: str = Field(max_length=1000)
    confidence: Confidence

    @field_validator("suggested_revision")
    @classmethod
    def draft_language_only(cls, value: str) -> str:
        banned = ("bạn không hiểu", "học viên không hiểu", "điểm số của bạn")
        if any(term in value.lower() for term in banned):
            raise ValueError("Suggested revision contains prohibited learner judgement")
        return value

    @model_validator(mode="after")
    def evidence_required_for_claims(self):
        if self.status in {ReviewStatus.misconception, ReviewStatus.missing_boundary, ReviewStatus.missing_concept} and not self.citations:
            raise ValueError("Misconception, missing_boundary and missing_concept require citations")
        if self.status != ReviewStatus.missing_concept and not self.note_excerpt.strip():
            raise ValueError("note_excerpt is required unless status is missing_concept")
        return self


class ReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    findings: list[Finding] = Field(min_length=1, max_length=12)
    provider: str = "unknown"
    is_mock: bool = False


class AIReviewPayload(BaseModel):
    """Strict schema returned by model providers before app metadata is attached."""

    model_config = ConfigDict(extra="forbid")
    findings: list[Finding] = Field(min_length=1, max_length=12)


class ReviewRequest(BaseModel):
    notes: str = Field(min_length=3, max_length=20000)
    lesson_id: str = Field(min_length=1, max_length=80)
    slide_number: int = Field(ge=1, le=500)
