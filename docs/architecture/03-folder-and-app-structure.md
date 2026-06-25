# 3. Folder Structure and Django App Structure

## 3.1 Target repository layout

The following is the intended structure after the foundation module is generated.
Empty placeholders are not created during the architecture phase; each folder
will arrive with the module that owns it.

```text
organicmart/
â”œâ”€â”€ .codex/
â”‚   â””â”€â”€ ...                         # Local agent/project guidance when needed
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â”œâ”€â”€ ci.yml                  # Lint, type, security, and test gates
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ accounts/
â”‚   â”œâ”€â”€ sellers/
â”‚   â”œâ”€â”€ catalog/
â”‚   â”œâ”€â”€ inventory/
â”‚   â”œâ”€â”€ promotions/
â”‚   â”œâ”€â”€ cart/
â”‚   â”œâ”€â”€ wishlist/
â”‚   â”œâ”€â”€ shipping/
â”‚   â”œâ”€â”€ orders/
â”‚   â”œâ”€â”€ payments/
â”‚   â”œâ”€â”€ reviews/
â”‚   â”œâ”€â”€ blog/
â”‚   â”œâ”€â”€ marketing/
â”‚   â”œâ”€â”€ notifications/
â”‚   â”œâ”€â”€ assistant/
â”‚   â””â”€â”€ analytics/
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ asgi.py
â”‚   â”œâ”€â”€ celery.py
â”‚   â”œâ”€â”€ urls.py
â”‚   â”œâ”€â”€ wsgi.py
â”‚   â””â”€â”€ settings/
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ base.py
â”‚       â”œâ”€â”€ local.py
â”‚       â”œâ”€â”€ test.py
â”‚       â””â”€â”€ production.py
â”œâ”€â”€ api/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ urls.py                     # /api/v1 route composition
â”‚   â”œâ”€â”€ schema.py                   # OpenAPI composition/customization
â”‚   â”œâ”€â”€ pagination.py
â”‚   â”œâ”€â”€ permissions.py              # Truly cross-domain API policies only
â”‚   â”œâ”€â”€ throttling.py
â”‚   â””â”€â”€ exceptions.py               # Stable API error envelope
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ base.html
â”‚   â”œâ”€â”€ layouts/
â”‚   â”œâ”€â”€ components/
â”‚   â”œâ”€â”€ partials/
â”‚   â”œâ”€â”€ registration/
â”‚   â”œâ”€â”€ errors/
â”‚   â””â”€â”€ emails/
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ css/
â”‚   â”‚   â”‚   â”œâ”€â”€ tokens.css
â”‚   â”‚   â”‚   â”œâ”€â”€ base.css
â”‚   â”‚   â”‚   â”œâ”€â”€ components.css
â”‚   â”‚   â”‚   â”œâ”€â”€ utilities.css
â”‚   â”‚   â”‚   â””â”€â”€ pages/
â”‚   â”‚   â”œâ”€â”€ js/
â”‚   â”‚   â”‚   â”œâ”€â”€ app.js
â”‚   â”‚   â”‚   â”œâ”€â”€ api-client.js
â”‚   â”‚   â”‚   â”œâ”€â”€ csrf.js
â”‚   â”‚   â”‚   â””â”€â”€ modules/
â”‚   â”‚   â””â”€â”€ images/
â”‚   â””â”€â”€ vendor/                     # Only audited vendored browser assets
â”œâ”€â”€ media/                          # Local development only; ignored by Git
â”œâ”€â”€ locale/                         # Translation files
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ integration/
â”‚   â”œâ”€â”€ e2e/
â”‚   â”œâ”€â”€ factories/
â”‚   â””â”€â”€ providers/
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ architecture/
â”‚   â”œâ”€â”€ api/
â”‚   â”œâ”€â”€ runbooks/
â”‚   â”œâ”€â”€ decisions/                  # Architecture decision records (ADRs)
â”‚   â””â”€â”€ learning/                   # Plain-language module explanations
â”œâ”€â”€ infra/
â”‚   â”œâ”€â”€ nginx/
â”‚   â”‚   â””â”€â”€ default.conf
â”‚   â”œâ”€â”€ gunicorn/
â”‚   â”‚   â””â”€â”€ gunicorn.conf.py
â”‚   â””â”€â”€ scripts/
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ wait_for_database.py
â”‚   â”œâ”€â”€ seed_development_data.py
â”‚   â””â”€â”€ check_migrations.py
â”œâ”€â”€ .editorconfig
â”œâ”€â”€ .env.example                   # Safe names/examples, never live secrets
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .pre-commit-config.yaml
â”œâ”€â”€ manage.py
â”œâ”€â”€ pyproject.toml                 # Tool configuration and project metadata
â”œâ”€â”€ requirements.in                # Direct runtime dependencies
â”œâ”€â”€ requirements.txt               # Fully pinned runtime lock
â”œâ”€â”€ requirements-dev.in
â”œâ”€â”€ requirements-dev.txt
â”œâ”€â”€ README.md
â””â”€â”€ SECURITY.md
```

The repository root shown above is the current workspace itself; there will not be
an unnecessary second nested `organicmart/` directory.

## 3.2 Standard app layout

Each substantial business app follows the same predictable shape:

```text
apps/catalog/
â”œâ”€â”€ __init__.py
â”œâ”€â”€ admin.py
â”œâ”€â”€ apps.py
â”œâ”€â”€ constants.py                   # Stable local constants, not business services
â”œâ”€â”€ models.py                      # Split into models/ package only when justified
â”œâ”€â”€ managers.py                    # Reusable manager/queryset behavior
â”œâ”€â”€ forms.py                       # HTML input validation
â”œâ”€â”€ services.py                    # Commands: create/change state
â”œâ”€â”€ selectors.py                   # Optimized reads/query composition
â”œâ”€â”€ policies.py                    # Authorization and business eligibility
â”œâ”€â”€ events.py                      # Explicit domain/application event definitions
â”œâ”€â”€ tasks.py                       # Thin, idempotent Celery task entry points
â”œâ”€â”€ urls.py                        # Server-rendered route names
â”œâ”€â”€ views.py                       # Thin HTML controllers
â”œâ”€â”€ api/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ serializers.py
â”‚   â”œâ”€â”€ permissions.py
â”‚   â”œâ”€â”€ filters.py
â”‚   â”œâ”€â”€ views.py
â”‚   â””â”€â”€ urls.py
â”œâ”€â”€ migrations/
â”‚   â””â”€â”€ __init__.py
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ catalog/
â”œâ”€â”€ static/
â”‚   â””â”€â”€ catalog/
â””â”€â”€ tests/
    â”œâ”€â”€ __init__.py
    â”œâ”€â”€ factories.py
    â”œâ”€â”€ test_models.py
    â”œâ”€â”€ test_services.py
    â”œâ”€â”€ test_selectors.py
    â”œâ”€â”€ test_policies.py
    â”œâ”€â”€ test_views.py
    â””â”€â”€ test_api.py
```

Small apps remain small. Files are split into packages only when their size or
ownership becomes difficult to navigate; â€œenterpriseâ€ code does not mean creating
an empty layer for every design-pattern name.

## 3.3 Responsibility of each file type

| File/type | Responsibility | Must avoid |
|---|---|---|
| Model | Persistence shape and local invariant | Provider calls, request objects, email sending |
| Manager/queryset | Reusable single-model filtering | Hidden cross-domain side effects |
| Form | HTML input parsing and user-facing validation | Duplicating transactional business logic |
| Serializer | API representation and input shape | Becoming an all-purpose checkout service |
| Service | State-changing use case and transaction boundary | Rendering responses or reading globals |
| Selector | Read/query composition and eager loading | Mutating state |
| Policy | Named authorization/eligibility decision | Depending only on a role string |
| View/API view | HTTP orchestration, response, status code | Pricing, stock, or payment rules |
| Task | Retry/idempotency wrapper around a service | Passing model instances through the broker |
| Adapter | External provider translation and timeout handling | Leaking provider response shapes into domain code |
| Template | Semantic, accessible presentation | Permissions, totals, or database queries |

## 3.4 Django app details

### `core`

Shared technical primitives only:

- Abstract UUID/time-stamped model bases.
- Typed service exceptions mapped to HTML/API responses.
- Correlation-ID middleware and health endpoints.
- Audit log model/service.
- Safe pagination/utilities with no domain ownership.
- Test helpers used across apps.

`core` must not become a miscellaneous home for code whose owner is unclear.

### `accounts`

- Custom email-based `User` model and manager.
- Registration, login/logout, email verification, password reset.
- Customer profile fields and address book.
- Session authentication for web; token entry endpoints coordinated by API config.
- Account status policies and user-owned profile/address services.

The initial migration is created before apps reference the user model. Changing to
a custom user halfway through a project is needlessly painful, so this decision is
made on day one.

### `sellers`

- Seller application and profile.
- Compliance document upload/review.
- Approval, rejection, suspension, and reactivation workflows.
- Seller storefront and dashboard shell.
- Seller-scoped permission policies.

Seller product, inventory, and order screens call their owning domain services;
the seller app does not duplicate those models.

### `catalog`

- Categories and bounded hierarchy.
- Product lifecycle, images, certifications, pricing fields, and approval.
- Product list/detail and category pages.
- Search, filtering, sorting, pagination, featured product selectors.
- Live search suggestions and SEO data.
- Search backend interface, initially implemented with PostgreSQL.

### `inventory`

- Stock record, append-only movement ledger, and checkout reservations.
- Atomic receive/adjust/reserve/release/confirm operations.
- Low-stock detection and seller alerts.
- Reservation expiry and reconciliation tasks.

Only inventory services modify stock quantities.

### `promotions`

- Coupon definitions, eligibility, validation, usage limits, and redemptions.
- Deterministic discount allocation to seller orders/items.
- Administration of active periods and category/seller restrictions.

A promotion result is a structured calculation; checkout never trusts a browser
discount value.

### `cart`

- Authenticated and guest carts, item updates, merge-on-login, expiry.
- Current-price cart summary through catalogue/promotion selectors.
- Add/update/remove endpoints and partial HTML/JSON responses.

Cart is an intent, not a financial record. It does not permanently snapshot price
and does not reserve stock.

### `wishlist`

- One user wishlist and idempotent add/remove/move-to-cart services.
- Product availability annotations for the wishlist page.

### `shipping`

- Shipping zones, methods, rates, and quote calculation.
- Provider-neutral tracking-link rules.
- Admin configuration and checkout quote selector.

Version one can use table-driven flat rates. A carrier adapter can later implement
real-time rates without changing checkout's interface.

### `orders`

- Checkout orchestration and immutable order snapshots.
- Multi-seller order partitions and order items.
- Explicit order/fulfilment state transitions.
- Customer order history/detail and seller fulfilment queue.
- Shipments, tracking, cancellations, return requests, and status history.

Order creation coordinates catalogue, inventory, promotion, shipping, and payment
interfaces inside deliberate transaction boundaries.

### `payments`

- Provider-neutral payment service protocol.
- Razorpay adapter, create-order flow, signature verification, and webhook inbox.
- Payment/refund state machines, idempotency, and reconciliation.
- No card handling or storage.

Provider SDK objects and names remain inside the adapter wherever possible.

### `reviews`

- Delivered-order-item eligibility.
- 1â€“5 star review creation/edit rules.
- Moderation and helpful votes.
- Rating distribution and average-summary rebuild.

### `blog`

- Categories, tags, post lifecycle, sanitized rich content, and SEO fields.
- Blog list/detail/category/search pages.
- Scheduled publish/unpublish behavior.
- Admin editor integration behind a sanitizer boundary.

### `marketing`

- Newsletter double opt-in and unsubscribe.
- Curated testimonials and homepage campaign content.
- Consent records and marketing-specific notification requests.

### `notifications`

- In-app notifications, user preferences, and delivery-attempt records.
- Event-to-template mapping for order confirmation, shipment updates, low stock,
  seller order alerts, and approval results.
- Email provider adapter and idempotent retry policy.

Domain apps decide that an event occurred; notifications decides how a subscribed
recipient is informed.

### `assistant`

- Floating-chat HTTP/API endpoints and conversation persistence.
- Product/policy context builder with allowlisted fields.
- Provider interface and Gemini adapter.
- Prompt-injection defenses, output validation, throttling, cost/latency logging,
  retention cleanup, and graceful fallback.

The assistant is advisory and read-only. It does not change carts, orders,
payments, accounts, or inventory in the first release.

### `analytics`

- Seller and administrator dashboard selectors.
- Daily aggregate read models and rebuild jobs.
- CSV report generation with access checks and expiring private downloads.

Dashboards read financial facts from confirmed orders/payments and clearly label
gross revenue, discounts, commission, refunds, and seller net amounts.

### Root `api`

This package composes domain API routes and cross-cutting API behavior. Domain
serializers and endpoints stay beside the domain they expose; a giant centralized
serializers file would erase module ownership.

## 3.5 Template organization

Reusable visual elements are includes with explicit context rather than copied
markup:

```text
templates/
â”œâ”€â”€ base.html
â”œâ”€â”€ layouts/
â”‚   â”œâ”€â”€ storefront.html
â”‚   â”œâ”€â”€ account.html
â”‚   â”œâ”€â”€ seller_dashboard.html
â”‚   â””â”€â”€ admin_dashboard.html
â”œâ”€â”€ components/
â”‚   â”œâ”€â”€ product_card.html
â”‚   â”œâ”€â”€ rating_stars.html
â”‚   â”œâ”€â”€ price.html
â”‚   â”œâ”€â”€ pagination.html
â”‚   â”œâ”€â”€ form_field.html
â”‚   â”œâ”€â”€ alert.html
â”‚   â”œâ”€â”€ empty_state.html
â”‚   â””â”€â”€ chatbot.html
â”œâ”€â”€ partials/
â”‚   â”œâ”€â”€ header.html
â”‚   â”œâ”€â”€ category_nav.html
â”‚   â”œâ”€â”€ messages.html
â”‚   â”œâ”€â”€ newsletter.html
â”‚   â””â”€â”€ footer.html
â”œâ”€â”€ registration/
â”œâ”€â”€ errors/
â”‚   â”œâ”€â”€ 400.html
â”‚   â”œâ”€â”€ 403.html
â”‚   â”œâ”€â”€ 404.html
â”‚   â”œâ”€â”€ 429.html
â”‚   â””â”€â”€ 500.html
â””â”€â”€ emails/
    â”œâ”€â”€ base.html
    â”œâ”€â”€ order_confirmation.html
    â”œâ”€â”€ shipment_update.html
    â””â”€â”€ seller_new_order.html
```

App-specific templates use namespaced paths such as
`apps/catalog/templates/catalog/product_detail.html`, preventing collisions.

## 3.6 Frontend structure and design system

Bootstrap supplies the responsive grid and accessible component baseline. A thin
OrganicMart design system supplies identity:

- Semantic tokens for forest, leaf, earth, surface, text, muted, success, warning,
  danger, focus, spacing, radius, shadow, and motion.
- Mobile-first breakpoints and touch targets of at least 44 CSS pixels.
- Local system font stack first for speed; optional brand font is subset/preloaded.
- Components remain usable under zoom, keyboard navigation, and reduced motion.
- Page JavaScript is loaded as ES modules or deferred modules, never inline.
- One Fetch wrapper applies CSRF, timeouts, JSON parsing, correlation IDs, and a
  consistent error shape.
- Content-generated elements are inserted with `textContent`; unsafe HTML
  insertion is not used for API or chatbot content.
- Images use width/height, responsive `srcset`, lazy loading below the fold, and
  optimized thumbnails produced asynchronously.

JavaScript modules will include live search, cart controls, wishlist actions,
checkout/Razorpay integration, review stars, seller charts, and the floating chat
widget. Each module must tolerate unavailable JavaScript/network and expose clear
loading/error/empty states.

## 3.7 Settings structure

`base.py` contains safe common settings. Environment files import base settings
and override only what differs.

- `local.py`: debug on, console email, local media, debug toolbar, permissive
  developer-only conveniences.
- `test.py`: deterministic password hasher, synchronous/fake task/provider
  adapters, isolated media, no network.
- `production.py`: debug off, required secret validation, secure cookies, HSTS,
  allowed hosts, proxy SSL header, object storage, real email, JSON logs, strict
  CSP/CORS, cache, and database connection configuration.

`DJANGO_SETTINGS_MODULE` selects the environment. If a required production
variable is absent, startup fails with the variable nameâ€”not its value.

## 3.8 Configuration contract (`.env.example`)

The eventual example file documents names without secrets:

```dotenv
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=replace-for-local-development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://organicmart:password@db:5432/organicmart
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
EMAIL_URL=consolemail://
DEFAULT_FROM_EMAIL=OrganicMart <noreply@example.com>
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
GEMINI_API_KEY=
GEMINI_MODEL_ALIAS=
MEDIA_STORAGE_BUCKET=
MEDIA_STORAGE_REGION=
SENTRY_DSN=
```

Exact settings and dependency versions will be validated against current official
documentation during implementation. `.env` is ignored; production secrets come
from the deployment platform's secret store.

## 3.9 Testing layout and strategy

Tests live next to domain code for discoverability, with cross-domain flows at the
repository level.

| Test level | Examples |
|---|---|
| Model/constraint | Invalid rating rejected, one primary image, nonnegative stock |
| Service | Seller approval, reserve/release stock, order transitions, review eligibility |
| Selector | Only active products, correct eager loading, stable pagination |
| Policy | Seller cannot edit another seller's product/order |
| View/API | CSRF/auth, validation, status codes, response contracts |
| Integration | Multi-seller checkout, Razorpay webhook idempotency, cancellation release |
| End-to-end | Register â†’ browse â†’ cart â†’ sandbox pay â†’ track â†’ review |
| Security | Upload validation, XSS payload, horizontal privilege escalation, throttling |
| Performance | Query budgets for home, product list, cart, seller order list |

Provider tests use contract-focused fake adapters and recorded safe fixture shapes;
the normal test suite never calls Razorpay, Gemini, email, or object storage over
the network.

## 3.10 Dependency and quality policy

- Runtime and development dependencies are separated and fully pinned.
- Direct dependencies are kept small and chosen for maintained, specific needs.
- Formatting, linting, import sorting, type checking, migration drift checks,
  Django deploy checks, dependency audit, and tests run in CI.
- Tests run against PostgreSQL, not SQLite, because constraints, search, locking,
  JSON, and indexes are PostgreSQL behavior.
- Migrations are reviewed like application code and roll-forward deployment is
  preferred.
- Public functions, services, policy decisions, and non-obvious invariants receive
  useful comments/docstrings. Comments explain **why**, not restate syntax.

## 3.11 Naming conventions

- Apps and Python modules: `snake_case`.
- Classes: `PascalCase`; functions/variables: `snake_case`.
- URL names: `app_namespace:verb_noun`, such as `catalog:product_detail`.
- API paths: plural nouns, lowercase, hyphen only where needed.
- Service commands: verbs (`place_order`, `reserve_stock`, `approve_product`).
- Selectors: intent-revealing reads (`products_visible_to_customer`).
- Boolean fields begin with `is`, `has`, `can`, or `allow`.
- Timestamps describe events (`approved_at`), not ambiguous names (`date2`).
- Database constraints and indexes receive stable explicit names.

## 3.12 Import and dependency direction

The desired direction is easy to remember:

```text
HTTP views/forms/serializers
          â†“
services, selectors, and policies
          â†“
models and provider interfaces
          â†“
PostgreSQL / Redis / provider adapters
```

If two apps repeatedly need each other's private models, that is a design signal:
introduce a public service/interface, move the concept to its real owner, or record
an explicit event. Circular imports are never â€œfixedâ€ by scattering imports inside
functions without examining the boundary problem.
