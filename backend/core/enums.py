from enum import StrEnum

class ScanStatus(StrEnum):
    """Enumeration of possible scan statuses."""
    VULNERABLE = "vulnerable"
    SAFE = "safe"
    ERROR = "error"

class Severity(StrEnum):
    """Enumeration of severity levels for vulnerabilities."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class TestType(StrEnum):
    """Enumeration of test types for security scans."""
    SQLI = "sqli"