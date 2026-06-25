"""Strict settings used by production web and worker processes."""

from django.core.exceptions import ImproperlyConfigured

from config.settings.base import *


def _require_secure_configuration() -> None:
    """Fail startup before serving traffic with unsafe production settings."""
    errors: list[str] = []

    if SECRET_KEY.startswith("unsafe-"):
        errors.append("DJANGO_SECRET_KEY must be set to a strong secret")
    if not ALLOWED_HOSTS or ALLOWED_HOSTS == ["localhost", "127.0.0.1"]:
        errors.append("DJANGO_ALLOWED_HOSTS must contain production hostnames")
    if not DATABASES["default"]["ENGINE"].endswith("postgresql"):
        errors.append("DATABASE_URL must use PostgreSQL")

    if errors:
        raise ImproperlyConfigured("; ".join(errors))


DEBUG = False
API_DOCS_ENABLED = env.bool("API_DOCS_ENABLED", default=False)

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int("DJANGO_HSTS_SECONDS", default=31_536_000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING["handlers"]["console"]["formatter"] = "json"

_require_secure_configuration()
