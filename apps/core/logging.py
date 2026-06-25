"""Logging helpers that avoid passing request objects throughout the codebase."""

import logging
from typing import Any

from apps.core.middleware import correlation_id_context


class CorrelationIdFilter(logging.Filter):
    """Add the current safe correlation ID to every structured log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_context.get()
        return True


def safe_log_context(**values: Any) -> dict[str, Any]:
    """Return explicit log fields; callers must never include secrets or PII."""
    return {key: value for key, value in values.items() if value is not None}
