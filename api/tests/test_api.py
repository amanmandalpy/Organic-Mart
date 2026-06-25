from http import HTTPStatus

from django.urls import reverse


def test_api_status_is_public_and_versioned(client):
    response = client.get(reverse("api:status"))

    assert response.status_code == HTTPStatus.OK
    assert response.json()["version"] == "v1"
    assert response.json()["request_id"] == response.headers["X-Request-ID"]


def test_unknown_api_route_uses_json_error_envelope(client):
    response = client.get(
        "/api/v1/does-not-exist/",
        headers={"Accept": "application/json"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "API endpoint not found.",
        "code": "not_found",
        "path": "/api/v1/does-not-exist/",
    }
