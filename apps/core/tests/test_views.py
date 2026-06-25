from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_renders(client):
    response = client.get(reverse("core:home"))

    assert response.status_code == HTTPStatus.OK
    assert "OrganicMart" in response.content.decode()
    assert response.headers["X-Request-ID"]


def test_liveness_does_not_require_database(client):
    response = client.get(reverse("core:health-live"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_readiness_checks_database_and_cache(client):
    response = client.get(reverse("core:health-ready"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "status": "ok",
        "components": {"database": "ok", "cache": "ok"},
    }


def test_unsafe_request_id_is_replaced(client):
    response = client.get(
        reverse("core:health-live"),
        headers={"X-Request-ID": "invalid request id with spaces"},
    )

    assert response.headers["X-Request-ID"] != "invalid request id with spaces"
