from __future__ import annotations
from typing import Any
from sqlalchemy.orm import Session
from core.enums import ScanStatus, Severity, TestType
from models.TestResult import TestResult

class TestResultRepository:
    """Repository for TestResult database operations."""

    @staticmethod
    def create_test_result(
        db: Session,
        scan_id: int,
        test_name: TestType,
        status: ScanStatus,
        severity: Severity,
        details: str,
        evidence_json: dict[str, Any],
        recommendations_json: list[str],
        commit: bool = True
    ) -> TestResult:
        """Create a new test result in the database."""

        new_test_result = TestResult(
            scan_id=scan_id,
            test_name=test_name,
            status=status,
            severity=severity,
            details=details,
            evidence_json=evidence_json,
            recommendations_json=recommendations_json
        )
        db.add(new_test_result)
        if commit:
            db.commit()
            db.refresh(new_test_result)
        return new_test_result
