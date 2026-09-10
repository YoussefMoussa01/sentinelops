"""Core constants and enumerations."""
from enum import Enum


class UserRole(str, Enum):
    """User roles."""

    SUPER_ADMIN = "SUPER_ADMIN"
    SOC_ADMIN = "SOC_ADMIN"
    SECURITY_ANALYST = "SECURITY_ANALYST"
    INVESTIGATOR = "INVESTIGATOR"
    VIEWER = "VIEWER"


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    """Alert status."""

    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class InvestigationStatus(str, Enum):
    """Investigation status."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class LogLevel(str, Enum):
    """Log event levels."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class TimelineEventType(str, Enum):
    """Timeline event types."""

    ALERT = "alert"
    LOGIN = "login"
    LOG = "log"
    NETWORK = "network"
    NOTE = "note"
    EVIDENCE = "evidence"
