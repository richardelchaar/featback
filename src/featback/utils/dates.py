"""Date and time utilities."""

from datetime import datetime, timezone

def utc_now() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)

def unix_to_datetime(timestamp: float) -> datetime:
    """Convert Unix timestamp to datetime."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
