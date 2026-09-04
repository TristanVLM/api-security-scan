from typing import Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from core.enums import (
    ScanStatus,
    Severity,
    TestType
)


class TestResultCreate(BaseModel):
    """Schema for creating a new test result."""
    test_name: TestType
    status: ScanStatus
    severity: Severity
    details: str
    evidence_json: dict[str, Any] = Field(default_factory=dict)
    recommendations_json: list[str] = Field(default_factory = list)

class TestResultResponse(BaseModel):
    """Schema for returning a test result."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    scan_id: int
    test_name: TestType
    status: ScanStatus
    severity: Severity
    details: str
    evidence_json: dict[str, Any]
    recommendations_json: list[str]
    created_at: datetime

    @property
    def is_vulnerable(self) -> bool:
        """Determine if the test result indicates a vulnerability."""
        return self.status == ScanStatus.VULNERABLE

    @property
    def is_high_severity(self) -> bool:
        """Determine if the test result indicates a high severity vulnerability."""
        return self.severity in {Severity.CRITICAL, Severity.HIGH}
