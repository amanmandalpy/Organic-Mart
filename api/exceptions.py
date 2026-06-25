"""Stable API errors that do not leak internal exception details."""

from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler


def organicmart_exception_handler(exc: Exception, context: dict[str, Any]):
    """Wrap DRF's safe error data in a predictable support-friendly envelope."""
    response: Response | None = exception_handler(exc, context)
    if response is None:
        return None

    request = context.get("request")
    correlation_id = getattr(request, "correlation_id", None)
    original_data = response.data

    if isinstance(original_data, dict) and "detail" in original_data:
        message = str(original_data["detail"])
        details: Any = None
    else:
        message = "The request could not be completed."
        details = original_data

    error_code = getattr(exc, "default_code", "request_error")
    response.data = {
        "error": {
            "code": str(error_code),
            "message": message,
            "details": details,
        },
        "correlation_id": correlation_id,
    }
    return response
