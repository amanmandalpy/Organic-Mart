"""Request correlation for logs and API error responses."""

import re
import uuid
from collections.abc import Callable
from contextvars import ContextVar, Token

from django.http import HttpRequest, HttpResponse

correlation_id_context: ContextVar[str] = ContextVar("correlation_id", default="-")
SAFE_CORRELATION_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


class CorrelationIdMiddleware:
    """Attach a safe request ID and return it to the caller for support."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        supplied = request.headers.get("X-Request-ID", "")
        correlation_id = (
            supplied if SAFE_CORRELATION_ID.fullmatch(supplied) else str(uuid.uuid4())
        )
        request.correlation_id = correlation_id  # type: ignore[attr-defined]
        token: Token[str] = correlation_id_context.set(correlation_id)

        try:
            response = self.get_response(request)
            response["X-Request-ID"] = correlation_id
            return response
        finally:
            correlation_id_context.reset(token)
