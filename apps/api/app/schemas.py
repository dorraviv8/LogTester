from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class AnalyzeRequest(BaseModel):
    log_text: str = Field(..., min_length=1, description="Raw log text pasted by the user")
    source: Optional[Literal["python", "java", "jenkins", "unknown"]] = Field(
        default="unknown",
        description="Optional hint about the log source"
    )


class AnalyzeResponse(BaseModel):
    error_type: Literal["python", "java", "jenkins", "unknown"]
    root_cause_summary: str
    most_likely_cause: str
    suggested_fixes: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    extracted_error_lines: List[str] = Field(default_factory=list)

