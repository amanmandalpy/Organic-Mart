from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_customer_can_register_and_is_logged_in(client):
    response = client.post(
        reverse("accounts:register"),
        {
            "first_name": "Asha",
            "last_name": "Green",
            "email": "asha@example.com",
            "phone_number": "9876543210",
            "password1": "Organic-pass-12345",
            "password2": "Organic-pass-12345",
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == reverse("accounts:profile")
    assert User.objects.filter(email="asha@example.com").exists()
    assert "_auth_user_id" in client.session


def test_customer_can_login_and_logout(client):
    User.objects.create_user("customer@example.com", "Organic-pass-12345")

    response = client.post(
        reverse("accounts:login"),
        {"username": "customer@example.com", "password": "Organic-pass-12345"},
    )

    assert response.status_code == HTTPStatus.FOUND
    assert "_auth_user_id" in client.session

    response = client.post(reverse("accounts:logout"))

    assert response.status_code == HTTPStatus.FOUND
    assert "_auth_user_id" not in client.session


def test_profile_requires_login(client):
    response = client.get(reverse("accounts:profile"))

    assert response.status_code == HTTPStatus.FOUND
    assert reverse("accounts:login") in response.headers["Location"]
