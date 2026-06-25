"""Cart values available in all templates."""

from typing import Any

from django.http import HttpRequest

from apps.cart.services import get_cart_summary


def cart_context(request: HttpRequest) -> dict[str, Any]:
    summary = get_cart_summary(request)
    return {
        "cart_item_count": summary.item_count,
        "cart_summary": summary,
    }
