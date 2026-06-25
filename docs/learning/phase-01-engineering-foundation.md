# Phase 1 learning notes: engineering foundation

This module creates the base a professional Django project stands on.

## What was built

- A Django project with separate settings for local, test, and production.
- A custom email-based `User` model created before other apps depend on users.
- Health endpoints for load balancers and deployment checks.
- API v1 wiring with JWT authentication available from day one.
- Bootstrap-based storefront shell and shared templates.
- Celery configuration for future background jobs.
- PostgreSQL-ready settings, Gunicorn, Nginx, and CI scaffolding.
- Ruff and pytest configuration so code quality can be checked repeatedly.

## Why this matters

Good engineering is not only writing features. It is making the project easy to
run, easy to test, easy to deploy, and hard to accidentally break.

The custom user model is especially important. Django lets you use the default
user model, but changing it later is painful. Real products usually need email
login, verification, phone numbers, and role-specific profiles, so we start with
the correct foundation.

## How to think like a software engineer here

Ask these questions before building features:

1. Can I run the project from a clean machine?
2. Can I prove the project boots?
3. Can I prove the code style is consistent?
4. Can I prove the database schema is versioned?
5. Can I deploy the same code shape to production?

That is why this phase added migrations, checks, tests, and runbooks
before adding products, carts, and checkout.

## Commands to remember

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

If those commands pass, you have a stable base for the next module.
