"""Developer-friendly settings. Never use this module in production."""

from config.settings.base import *

DEBUG = True
API_DOCS_ENABLED = True

# Beginner-friendly fallback:
#
# If you run `python manage.py runserver` directly from the virtual environment
# and have not configured DATABASE_URL, use a local SQLite database. Production
# settings still require PostgreSQL, so the real deployment architecture remains
# PostgreSQL-first.
if env("DATABASE_URL", default=None) is None:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Same idea for cache: no Redis is required for a simple local runserver.
if env("CACHE_URL", default=None) is None:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "organicmart-local-dev",
        }
    }

# A fast console formatter is easier to read while learning locally.
LOGGING["handlers"]["console"]["formatter"] = "console"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
