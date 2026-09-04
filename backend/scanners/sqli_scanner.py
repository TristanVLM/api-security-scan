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

        boolean_based_test = self._test_boolean_based_sqli()
        if boolean_based_test["vulnerable"]:
            return self._create_vulnerable_result(
                details="Boolean-based SQL Injection detected",
                evidence=boolean_based_test,
                severity=Severity.CRITICAL,
                recommendations=[
                    "Use parameterized queries for all database operations",
                    "Implement proper input validation",
                    "Avoid exposing different responses for true/false conditions",
                ]
            )

        time_based_test = self._test_time_based_sqli()
        if time_based_test["vulnerable"]:
            return self._create_vulnerable_result(
                details=f"Time-based SQL Injection detected: {time_based_test['database_type']}",
                evidence=time_based_test,
                severity=Severity.CRITICAL,
                recommendations=[
                    "Use parameterized queries exclusively",
                    "Implement strict input validation",
                    "Monitor for unusual response time patterns",
                ]
            )

        return TestResultCreate(
            test_name=TestType.SQLI,
            status=ScanStatus.SAFE,
            severity=Severity.INFO,
            details="No SQL Injection vulnerabilities detected",
            evidence_json={
                "error_based_test": error_based_test,
                "boolean_based_test": boolean_based_test,
                "time_based_test": time_based_test
            },
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

    def _test_boolean_based_sqli(self) -> dict[str, Any]:
        """Test for boolean-based SQL Injection vulnerabilities."""
        try:
            baseline_response = self.make_request("GET", "/?id=1")
            baseline_length = len(baseline_response.text)
            baseline_status = baseline_response.status_code

            if baseline_status != 200:
                return {
                    "vulnerable": False,
                    "description": f"Baseline request failed",
                    "baseline_status": baseline_status,
                }

            boolean_payloads = SQLiPayloads.BOOLEAN_BASED_BLIND

            true_payloads  = [p for p in boolean_payloads if "AND '1'='1" in p or "AND 1=1" in p]
            false_payloads = [p for p in boolean_payloads if "AND '1'='2" in p or "AND 1=2" in p or "AND 1=0" in p]

            true_lengths  = []
            for payload in true_payloads:
                response = self.make_request("GET", f"/?id={payload}")
                true_lengths.append(len(response.text))

            false_lengths = []
            for payload in false_payloads:
                response = self.make_request("GET", f"/?id={payload}")
                false_lengths.append(len(response.text))

            # Calculate the average lengths for true and false payloads
            avg_true  = statistics.mean(true_lengths) if true_lengths else 0
            avg_false = statistics.mean(false_lengths) if false_lengths else 0

            length_difference = abs(avg_true - avg_false)

            # Significant difference in response lengths indicates a potential boolean-based SQLi vulnerability
            if length_difference > 100 and avg_true != avg_false:
                return {
                    "vulnerable": True,
                    "baseline_length": baseline_length,
                    "true_condition_avg_length": avg_true,
                    "false_condition_avg_length": avg_false,
                    "length_difference": length_difference,
                    "confidence": "HIGH" if length_difference > 500 else "MEDIUM",
                }
            return {
                "vulnerable": False,
                "description": "No boolean-based SQLi detected",
                "length_difference": length_difference,
            }
        except Exception as e:
            return {
                "vulnerable": False,
                "error": str(e),
                "description": "Error testing boolean-based SQLi",
            }

    def _test_time_based_sqli(self, delay_seconds: int = 5) -> dict[str, Any]:
        """Test for time-based SQL Injection vulnerabilities."""
        try:
            baseline_mean, baseline_stdev = self.get_baseline_timing("/")

            threshold = baseline_mean + (3 * baseline_stdev)
            expected_delay_time = baseline_mean + delay_seconds

            all_time_payloads = SQLiPayloads.TIME_BASED_BLIND

            delay_payloads = {
                "mysql": [p for p in all_time_payloads if "SLEEP" in p],
                "postgresql": [p for p in all_time_payloads if "pg_sleep" in p],
                "mssql": [p for p in all_time_payloads if "WAITFOR" in p],
            }

            for db_type, payloads in delay_payloads.items():
                for payload in payloads:
                    delay_times = []

                    for _ in range(3):  # Test each payload 3 times
                        try:
                            response = self.make_request("GET", f"/?id={payload}", timeout=delay_seconds + 10)
                            elapsed = getattr(response, "request_time", 0.0)
                            delay_times.append(elapsed)
                        except Exception:
                            delay_times.append(delay_seconds + 10)  # Assume max delay if request fails
                        time.sleep(1) # Short pause between requests

                    avg_delay = statistics.mean(delay_times)

                    if avg_delay > expected_delay_time - 1:
                        confidence = "HIGH" if avg_delay > expected_delay_time else "MEDIUM"

                        return {
                            "vulnerable": True,
                            "database_type": db_type,
                            "payload": payload,
                            "baseline_time": f"{baseline_mean:.3f}s",
                            "response_time": f"{avg_delay:.3f}s",
                            "expected_delay_time": f"{expected_delay_time:.3f}s",
                            "confidence": confidence,
                            "individual_times": [f"{t:.3f}s" for t in delay_times]
                        }
            return {
                "vulnerable": False,
                "baseline_time": f"{baseline_mean:.3f}s",
                "threshold": f"{threshold:.3f}s",
                "description": "No time-based SQLi detected"
            }
        except Exception as e:
            return {
                "vulnerable": False,
                "error": str(e),
                "description": "Error testing time-based SQLi",
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