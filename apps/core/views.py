"""Foundation HTML and health-check views."""

from http import HTTPStatus

from django.core.cache import cache
from django.db import connections
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from apps.blog.selectors import latest_blog_posts
from apps.catalog.selectors import (
    active_products,
    featured_categories,
    featured_products,
)

SPOTLIGHT_IMAGE_PATHS = [
    "src/img/spotlight/seasonal-greens.png",
    "src/img/spotlight/seasonal-fruits.png",
    "src/img/spotlight/honey-herbal.png",
    "src/img/spotlight/grains-spices.png",
]


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    """Render the storefront homepage."""
    featured = list(featured_products(limit=6))
    spotlight_products = list(active_products()[:12])
    spotlight_slides = [
        {
            "product": product,
            "fallback_image": SPOTLIGHT_IMAGE_PATHS[index % len(SPOTLIGHT_IMAGE_PATHS)],
        }
        for index, product in enumerate(spotlight_products)
    ]
    return render(
        request,
        "core/home.html",
        {
            "featured_categories": featured_categories()[:8],
            "featured_products": featured,
            "spotlight_slides": spotlight_slides,
            "latest_posts": latest_blog_posts(),
        },
    )


@require_GET
def sell_center(request: HttpRequest) -> HttpResponse:
    """Show the seller center landing page."""
    return render(request, "core/sell_center.html")


@require_GET
def order_success(request: HttpRequest) -> HttpResponse:
    return render(request, "core/order_success.html")


@never_cache
@require_GET
def health_live(request: HttpRequest) -> JsonResponse:
    """Prove only that the Django process can answer an HTTP request."""
    del request
    return JsonResponse({"status": "ok"})


@never_cache
@require_GET
def health_ready(request: HttpRequest) -> JsonResponse:
    """Check essential dependencies without exposing connection details."""
    del request
    components: dict[str, str] = {}

    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        components["database"] = "ok"
    except Exception:  # Health endpoints report state; logs capture diagnostics.
        components["database"] = "unavailable"

    try:
        probe_key = "organicmart:health:ready"
        cache.set(probe_key, "ok", timeout=10)
        components["cache"] = "ok" if cache.get(probe_key) == "ok" else "unavailable"
    except Exception:
        components["cache"] = "unavailable"

    is_ready = all(value == "ok" for value in components.values())
    return JsonResponse(
        {"status": "ok" if is_ready else "unavailable", "components": components},
        status=HTTPStatus.OK if is_ready else HTTPStatus.SERVICE_UNAVAILABLE,
    )


def bad_request(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    del exception
    return render(request, "errors/400.html", status=HTTPStatus.BAD_REQUEST)


def permission_denied(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    del exception
    return render(request, "errors/403.html", status=HTTPStatus.FORBIDDEN)


def page_not_found(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    del exception
    return render(request, "errors/404.html", status=HTTPStatus.NOT_FOUND)


def server_error(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "errors/500.html",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
