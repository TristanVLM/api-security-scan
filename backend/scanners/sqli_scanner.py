import time
import statistics
from typing import Any

from core.enums import (
    ScanStatus,
    Severity,
    TestType
)

from schemas.test_result_schemas import TestResultCreate

from .payloads import SQLiPayloads
from .base_scanner import BaseScanner

class SQLiScanner(BaseScanner):
    """Scanner for detecting SQL Injection vulnerabilities."""

    def scan(self) -> TestResultCreate:
        """Perform the SQL Injection scan and return a TestResultCreate object."""
        error_based_test = self._test_error_based_sqli()
        if error_based_test["vulnerable"]:
            return self._create_vulnerable_result(
                details= f"Error-based SQL Injection detected: {error_based_test['database_type']}",
                evidence=error_based_test,
                severity=Severity.CRITICAL,
                recommendations=[
                    "Use parameterized queries (prepared statements)",
                    "Never concatenate user input into SQL queries",
                    "Implement input validation and sanitization",
                    "Disable detailed error messages in production",
                    "Use ORM frameworks with proper escaping",
                ]
            )

        return TestResultCreate(
            test_name=TestType.SQLI,
            status=ScanStatus.SAFE,
            severity=Severity.INFO,
            details="No SQL Injection vulnerabilities detected",
            evidence_json=error_based_test,
            recommendations_json=[
                "Continue using parameterized queries",
                "Regularly review and update security practices",
            ]
        )

    def _test_error_based_sqli(self) -> dict[str, Any]:
        """Test for error-based SQL Injection vulnerabilities."""
        error_signatures = SQLiPayloads.get_error_signatures()

        basic_payloads = SQLiPayloads.BASIC_AUTHENTICATION_BYPASS

        for payload in basic_payloads:
            try:
                response = self.make_request("GET", f"/?id={payload}")
                response_text = response.text.lower()

                for db_type, signatures in error_signatures.items():
                    for signature in signatures:
                        if signature in response_text:
                            return {
                                "vulnerable": True,
                                "database_type": db_type,
                                "payload": payload,
                                "status_code": response.status_code,
                                "error_signature": signature,
                                "response_excerpt": response_text[:500]
                            }
            except Exception:
                continue # A network error is not always indicative of an SQLi vulnerability

        return {
            "vulnerable": False,
            "payload_tested": len(basic_payloads),
            "description": "No database error detected"
        }

    def _create_vulnerable_result(
        self,
        details: str,
        evidence: dict[str, Any],
        severity: Severity = Severity.CRITICAL,
        recommendations: list[str] | None = None
    ) -> TestResultCreate:
        """Create a TestResultCreate object for a vulnerable SQL Injection test."""

        return TestResultCreate(
            test_name=TestType.SQLI,
            status=ScanStatus.VULNERABLE,
            severity=severity,
            details=details,
            evidence_json=evidence,
            recommendations_json=recommendations or []
        )