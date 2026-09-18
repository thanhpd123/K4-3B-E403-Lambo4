from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ReviewStatus(str, Enum):
    correct_complete = "correct_complete"
    misconception = "misconception"
    missing_boundary = "missing_boundary"
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
    note_excerpt: str = Field(min_length=1, max_length=1500)
    finding: str = Field(min_length=1, max_length=1500)
    explanation: str = Field(min_length=1, max_length=2500)
    citations: list[Citation] = Field(default_factory=list, max_length=5)
    suggested_revision: str = Field(default="", max_length=2500)
    review_question: str = Field(default="", max_length=1000)
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
        if self.status in {ReviewStatus.misconception, ReviewStatus.missing_boundary} and not self.citations:
            raise ValueError("Misconception and missing_boundary require citations")
        return self


class ReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    findings: list[Finding] = Field(min_length=1, max_length=12)
    provider: str = "unknown"
    is_mock: bool = False


class ReviewRequest(BaseModel):
    notes: str = Field(min_length=3, max_length=20000)
    source_text: str = Field(min_length=20, max_length=120000)
    source_type: str = Field(default="transcript", pattern=r"^(transcript|slide)$")

