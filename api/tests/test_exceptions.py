from http import HTTPStatus

from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.test import APIRequestFactory

from api.exceptions import organicmart_exception_handler


def test_exception_handler_wraps_safe_detail_errors():
    request = APIRequestFactory().get("/api/v1/orders/")
    request.correlation_id = "req-test-123"

    response = organicmart_exception_handler(
        NotAuthenticated(),
        {"request": request},
    )

    assert response is not None
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"
    assert response.data["error"]["details"] is None
    assert response.data["correlation_id"] == "req-test-123"


def test_exception_handler_preserves_validation_details():
    response = organicmart_exception_handler(
        ValidationError({"email": ["This field is required."]}),
        {},
    )

    assert response is not None
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data["error"]["code"] == "invalid"
    assert response.data["error"]["message"] == "The request could not be completed."
    assert "email" in response.data["error"]["details"]


def test_exception_handler_returns_none_for_unhandled_exceptions():
    assert organicmart_exception_handler(RuntimeError("boom"), {}) is None
