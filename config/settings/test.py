"""Fast, deterministic settings for automated tests."""

from config.settings.base import *

DEBUG = False
API_DOCS_ENABLED = True
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "organicmart-tests",
    }
}
STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

# CI can supply PostgreSQL through DATABASE_URL. For local learning, if no
# explicit DATABASE_URL is provided we default to SQLite so `pytest` works
# without a local PostgreSQL password.
if env("DATABASE_URL", default=None) is None or env.bool(
    "ALLOW_SQLITE_FOR_TESTS",
    default=False,
):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
