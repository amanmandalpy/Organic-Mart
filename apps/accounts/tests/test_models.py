import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_user_is_created_with_normalized_email():
    user = User.objects.create_user("  Builder@Example.COM ", "safe-test-pass-123")

    assert user.email == "builder@example.com"
    assert user.check_password("safe-test-pass-123")
    assert not user.is_staff


def test_email_is_case_insensitively_unique():
    User.objects.create_user("builder@example.com", "safe-test-pass-123")

    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create_user("BUILDER@example.com", "safe-test-pass-456")


def test_superuser_requires_staff_flags():
    with pytest.raises(ValueError, match="is_staff"):
        User.objects.create_superuser(
            "admin@example.com",
            "safe-test-pass-123",
            is_staff=False,
        )


def test_superuser_requires_superuser_flag():
    with pytest.raises(ValueError, match="is_superuser"):
        User.objects.create_superuser(
            "admin@example.com",
            "safe-test-pass-123",
            is_superuser=False,
        )


def test_user_requires_email():
    with pytest.raises(ValueError, match="email"):
        User.objects.create_user("", "safe-test-pass-123")
