# Security policy

OrganicMart is a portfolio project built with production-minded security
practices. Treat it like a real ecommerce system while developing.

## Supported versions

Only the current `main` branch is supported during active development.

## Secret handling

- Never commit `.env` files.
- Never commit real Razorpay, Gemini, email, database, or cloud credentials.
- Rotate any secret that is accidentally shared.
- Use `.env.example` only for safe placeholder values.

## Baseline protections

The foundation includes:

- Django CSRF protection.
- Secure password hashing through Django.
- Django ORM query parameterization.
- Clickjacking protection.
- Content Security Policy configuration.
- HTTP security headers.
- JWT access/refresh token configuration for APIs.
- Environment-specific production startup validation.

## Reporting a vulnerability

If this were a public project, vulnerabilities would be reported privately to
the maintainer. For this learning project, record issues in a private note or
GitHub issue and fix them before sharing the repository.
