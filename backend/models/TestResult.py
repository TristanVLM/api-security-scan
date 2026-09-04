from sqlalchemy import Column, Enum, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from core.enums import (
    ScanStatus,
    Severity,
    TestType
)

from .Base import BaseModel

class TestResult(BaseModel):
    """ Store individual test results for a scan."""

    __tableName__ = "test_results"

    scan_id = Column(
        Integer,
        ForeignKey("scans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    test_name = Column(
        Enum(TestType),
        nullable=False,
        index=True,
    )

    status = Column(
        Enum(ScanStatus),
        nullable=False,
        index=True,
    )

    severity = Column(
        Enum(Severity),
        nullable=False,
        index=True,
    )

    details = Column(Text, nullable=False)
    evidence_json = Column(JSON, nullable=False, default=dict)
    recommendations_json = Column(JSON, nullable=False, default=list)

    scan = relationship("Scan", back_populates="test_results")

    def __repr__(self) -> str:
        return (
            f"<TestResult(id={self.id}, test_name={self.test_name.value}, "
            f"status={self.status.value})>"
        )

    @property
    def is_vulnerable(self) -> bool:
        """Determine if the test result indicates a vulnerability."""
        return self.status.value == ScanStatus.VULNERABLE

    @property
    def is_high_severity(self) -> bool:
        """Determine if the test result indicates a high severity vulnerability."""
        return self.severity.value in {Severity.CRITICAL, Severity.HIGH}
