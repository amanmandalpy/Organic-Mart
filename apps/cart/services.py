"""Session-backed cart and wishlist services.

This keeps the cart usable before account-based carts are introduced. Later,
the same view flow can be moved to database-backed carts per authenticated user.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from django.http import HttpRequest

from apps.catalog.models import Product

CART_SESSION_KEY = "organicmart_cart"
WISHLIST_SESSION_KEY = "organicmart_wishlist"
COUPON_SESSION_KEY = "organicmart_coupon"
STARTER_COUPON_CODE = "ORGANIC10"


@dataclass(frozen=True)
class CartLine:
    product: Product
    quantity: int
    line_total: Decimal


@dataclass(frozen=True)
class CartSummary:
    lines: list[CartLine]
    subtotal: Decimal
    discount: Decimal
    shipping: Decimal
    total: Decimal
    item_count: int
    coupon_code: str


def _cart(request: HttpRequest) -> dict[str, int]:
    return request.session.setdefault(CART_SESSION_KEY, {})


def _wishlist(request: HttpRequest) -> list[str]:
    return request.session.setdefault(WISHLIST_SESSION_KEY, [])


def add_product(request: HttpRequest, product: Product, quantity: int = 1) -> None:
    cart = _cart(request)
    product_key = str(product.pk)
    existing_quantity = int(cart.get(product_key, 0))
    cart[product_key] = min(existing_quantity + max(quantity, 1), product.stock)
    request.session.modified = True


def update_product(request: HttpRequest, product: Product, quantity: int) -> None:
    cart = _cart(request)
    product_key = str(product.pk)
    if quantity <= 0:
        cart.pop(product_key, None)
    else:
        cart[product_key] = min(quantity, product.stock)
    request.session.modified = True


def remove_product(request: HttpRequest, product: Product) -> None:
    _cart(request).pop(str(product.pk), None)
    request.session.modified = True


def clear_cart(request: HttpRequest) -> None:
    request.session[CART_SESSION_KEY] = {}
    request.session[COUPON_SESSION_KEY] = ""
    request.session.modified = True


def apply_coupon(request: HttpRequest, code: str) -> bool:
    normalized = code.strip().upper()
    if normalized == STARTER_COUPON_CODE:
        request.session[COUPON_SESSION_KEY] = STARTER_COUPON_CODE
        request.session.modified = True
        return True
    request.session[COUPON_SESSION_KEY] = ""
    request.session.modified = True
    return False


def add_to_wishlist(request: HttpRequest, product: Product) -> None:
    wishlist = _wishlist(request)
    product_key = str(product.pk)
    if product_key not in wishlist:
        wishlist.append(product_key)
        request.session.modified = True


def remove_from_wishlist(request: HttpRequest, product: Product) -> None:
    wishlist = _wishlist(request)
    product_key = str(product.pk)
    if product_key in wishlist:
        wishlist.remove(product_key)
        request.session.modified = True


def get_wishlist_products(request: HttpRequest):
    product_ids = _wishlist(request)
    return Product.objects.filter(pk__in=product_ids, status=Product.Status.ACTIVE)


def get_cart_summary(request: HttpRequest) -> CartSummary:
    cart_data: dict[str, Any] = _cart(request)
    product_ids = list(cart_data.keys())
    products = Product.objects.filter(pk__in=product_ids, status=Product.Status.ACTIVE)
    products_by_id = {str(product.pk): product for product in products}

    lines: list[CartLine] = []
    for product_id, raw_quantity in cart_data.items():
        product = products_by_id.get(str(product_id))
        if product is None:
            continue
        quantity = min(max(int(raw_quantity), 1), product.stock)
        lines.append(
            CartLine(
                product=product,
                quantity=quantity,
                line_total=product.final_price * quantity,
            )
        )

    subtotal = sum((line.line_total for line in lines), Decimal("0.00"))
    coupon_code = request.session.get(COUPON_SESSION_KEY, "")
    discount = Decimal("0.00")
    if coupon_code == STARTER_COUPON_CODE and subtotal > 0:
        discount = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))

    shipping = (
        Decimal("0.00")
        if subtotal >= Decimal("999.00") or subtotal == 0
        else Decimal("49.00")
    )
    total = (subtotal - discount + shipping).quantize(Decimal("0.01"))
    item_count = sum(line.quantity for line in lines)

    return CartSummary(
        lines=lines,
        subtotal=subtotal.quantize(Decimal("0.01")),
        discount=discount,
        shipping=shipping,
        total=total,
        item_count=item_count,
        coupon_code=coupon_code,
    )
