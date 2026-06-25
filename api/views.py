"""Small API surface proving the versioned delivery layer is wired."""

from http import HTTPStatus

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class FoundationStatusAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "anon"

    def get(self, request: Request) -> Response:
        return Response(
            {
                "name": "OrganicMart API",
                "version": "v1",
                "status": "ok",
                "request_id": getattr(request, "correlation_id", None),
            }
        )


class APINotFoundAPIView(APIView):
    """Return a consistent JSON envelope for unmatched API routes."""

    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "anon"

    def get(self, request: Request, unmatched_path: str = "") -> Response:
        del request
        return Response(
            {
                "detail": "API endpoint not found.",
                "code": "not_found",
                "path": f"/api/v1/{unmatched_path}",
            },
            status=HTTPStatus.NOT_FOUND,
        )

    post = put = patch = delete = get
