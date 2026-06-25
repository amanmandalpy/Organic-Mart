<<<<<<< HEAD
# OrganicMart

OrganicMart is a production-oriented organic products marketplace built with
Django, Bootstrap, PostgreSQL-ready settings, session cart flows, admin-managed
catalogue content, customer authentication, and a clean storefront UI.

The project is designed as a resume and interview project, so the codebase
follows a modular Django structure, environment-based settings, reusable
services/selectors, migrations, tests, and Ubuntu deployment notes.

## Current Status

OrganicMart is now client-showcase ready for the main storefront flow:

- Customers can register, login, logout, and update their profile.
- Products, categories, reviews, prices, stock, discounts, and images are
  managed from the Django admin panel.
- Product cards and detail pages support real uploaded images with responsive
  automatic cropping.
- Homepage includes category tiles, featured products, a seasonal image slider,
  latest blog posts, newsletter UI, seller center, and trust sections.
- Cart, wishlist, coupon, checkout, and order-success pages are working with
  session storage.
- Blog posts, blog categories, tags, featured images, SEO title, SEO
  description, publish/unpublish workflow, and admin moderation are available.
- API v1 base route and JWT token routes are wired with Django REST Framework.
- Gunicorn, Nginx, health checks, static files, and production settings are
  included for deployment preparation.

## Tech Stack

- Backend: Python, Django 5, Django REST Framework
- Database: PostgreSQL in production, SQLite fallback for simple local runserver
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
- Auth: Django custom user model with email login
- Admin: Django admin for users, products, reviews, categories, blogs, tags
- API Auth: Simple JWT token endpoints
- Deployment: Ubuntu VPS, Python virtual environment, Gunicorn, Nginx
- Quality: Pytest, Ruff linting/formatting, Django system checks

## Main Apps

- `apps.accounts`: custom email user model, registration, login, logout, profile
- `apps.catalog`: categories, products, reviews, product images, product search
- `apps.cart`: session cart, wishlist, coupon, checkout, order success flow
- `apps.blog`: admin-managed blogs, categories, tags, SEO fields, publish status
- `apps.core`: homepage, seller center, health checks, shared public pages
- `api`: versioned API foundation and JWT endpoints

## Important URLs

Run the server and open these pages:

- Storefront: `http://127.0.0.1:8000/`
- Products: `http://127.0.0.1:8000/products/`
- Blog: `http://127.0.0.1:8000/blog/`
- Register: `http://127.0.0.1:8000/accounts/register/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Profile: `http://127.0.0.1:8000/accounts/profile/`
- Cart: `http://127.0.0.1:8000/cart/`
- Admin: `http://127.0.0.1:8000/admin/`
- API status: `http://127.0.0.1:8000/api/v1/`

## Local Setup

For your Windows local setup:

```powershell
cd C:\Users\admin\Documents\organic
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

If the server is already running, refresh the browser at:

```text
http://127.0.0.1:8000/
```

## Admin Panel Guide

Create a superuser:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then login at:

```text
http://127.0.0.1:8000/admin/
```

Admin can manage:

- Users from `Accounts > Users`
- Product categories from `Catalog > Categories`
- Products and uploaded images from `Catalog > Products`
- Reviews from `Catalog > Product reviews`
- Blog categories from `Blog > Blog categories`
- Tags from `Blog > Blog tags`
- Blog posts from `Blog > Blog posts`

To upload a real product image:

1. Open `Admin > Catalog > Products`.
2. Click a product.
3. Upload the image in the `Image` field.
4. Save.
5. Refresh the storefront. The product card, product detail page, cart, and
   slider will automatically size and crop the image.

To publish a blog:

1. Open `Admin > Blog > Blog posts`.
2. Create or edit a post.
3. Set `Status` to `Published`.
4. Add `Published at`, SEO title, SEO description, category, tags, and image.
5. Save. The post appears on `/blog/` and the homepage latest blogs section.

## User Flow

Customer journey:

1. User registers with name, email, phone, and password.
2. User is logged in automatically after registration.
3. User browses categories and products.
4. User views product details, images, ingredients, benefits, reviews, and stock.
5. User adds products to cart or wishlist.
6. User applies coupon `ORGANIC10`.
7. User checks out and sees the order confirmation page.
8. User can return to profile/cart/wishlist/product pages from the navbar.

Admin/editor journey:

1. Admin logs into `/admin/`.
2. Admin creates categories, products, reviews, blog categories, tags, and posts.
3. Admin uploads product and blog images.
4. Admin controls publish status for blog posts.
5. Storefront updates automatically from database content.

## Architecture Notes

OrganicMart uses a modular monolith. This is a strong Django architecture for a
portfolio ecommerce project because it keeps development simple while still
separating business capabilities.

Important design decisions:

- A custom user model was created early to avoid painful auth migrations later.
- Product and blog reads use selectors so templates do not own complex queries.
- Cart and wishlist logic lives in services, not templates.
- Admin image previews make content management easier.
- Uploaded images use `ImageField` and CSS `object-fit: cover` for clean UI.
- Health endpoints exist for deployment monitoring.
- Settings are split into base, local, test, and production.
- Secrets come from environment variables through `.env`.
- JWT endpoints are ready for future frontend/mobile API use.

## Database Modules

Core implemented models:

- `accounts.User`: email-based user, profile fields, verification fields, status
- `catalog.Category`: product category, slug, icon, featured status
- `catalog.Product`: product details, price, discount, stock, SKU, image,
  certification, benefits, ingredients, rating summary, status
- `catalog.ProductReview`: rating, title, review body, verified purchase flag
- `blog.BlogCategory`: blog grouping and display order
- `blog.BlogTag`: reusable article tags
- `blog.BlogPost`: title, slug, excerpt, content, featured image, SEO fields,
  status, published date, author, tags

## Quality Commands

Use these before showing the project or deploying:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pytest
```

## Deployment Preparation

The repo includes:

- `infra/gunicorn/gunicorn.conf.py`
- `infra/nginx/default.conf`
- `docs/runbooks/deployment.md`
- `docs/runbooks/razorpay-payment-gateway.md`

Before real live deployment:

1. Set `DJANGO_SECRET_KEY` to a strong secret.
2. Set `DJANGO_ALLOWED_HOSTS` to your domain.
3. Use PostgreSQL in `DATABASE_URL`.
4. Set `DEBUG=False`.
5. Run migrations.
6. Run collectstatic.
7. Create superuser.
8. Configure email provider.
9. Configure HTTPS/TLS through Nginx or a cloud load balancer.
10. Configure media file storage for production uploads.
11. Add real Razorpay keys before accepting real payments.
12. Back up PostgreSQL before releases.

## Interview Talking Points

- Why a modular monolith is a good first production architecture.
- Why custom user models should be created at project start.
- How Django protects against CSRF, SQL injection, XSS, and auth issues.
- Why services/selectors make code easier to test and scale.
- How admin-managed blog content supports SEO and business users.
- How image uploads are handled with Django media and responsive CSS.
- How environment-based settings prepare the same codebase for local, test, and
  production.
- How Gunicorn, Nginx, PostgreSQL, and health checks fit into deployment.
- How Razorpay can be connected using the payment gateway runbook.

## Architecture Documents

- [Software architecture](docs/architecture/01-software-architecture.md)
- [Database design](docs/architecture/02-database-design.md)
- [Folder and Django app structure](docs/architecture/03-folder-and-app-structure.md)
- [Development roadmap](docs/architecture/04-development-roadmap.md)
- [Local development runbook](docs/runbooks/local-development.md)
- [Deployment guide](docs/runbooks/deployment.md)
- [Razorpay payment gateway guide](docs/runbooks/razorpay-payment-gateway.md)
=======
# Organic-Mart
>>>>>>> bb128c8f7e8395ac957390a66c835981c49103e8
