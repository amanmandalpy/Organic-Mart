"""Public cart, wishlist, and checkout views."""

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.cart import services
from apps.catalog.models import Product


def cart_detail(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cart/detail.html",
        {"summary": services.get_cart_summary(request)},
    )


@require_POST
def add_to_cart(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id, status=Product.Status.ACTIVE)
    quantity = int(request.POST.get("quantity", "1"))
    if not product.is_in_stock:
        messages.warning(request, f"{product.name} is currently out of stock.")
        return redirect(product)

    services.add_product(request, product, quantity)
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart:detail")


@require_POST
def update_cart(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id, status=Product.Status.ACTIVE)
    quantity = int(request.POST.get("quantity", "1"))
    services.update_product(request, product, quantity)
    messages.success(request, "Cart updated.")
    return redirect("cart:detail")


@require_POST
def remove_from_cart(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id, status=Product.Status.ACTIVE)
    services.remove_product(request, product)
    messages.info(request, f"{product.name} removed from cart.")
    return redirect("cart:detail")


@require_POST
def apply_coupon_view(request: HttpRequest) -> HttpResponse:
    coupon = request.POST.get("coupon", "")
    if services.apply_coupon(request, coupon):
        messages.success(request, "Coupon ORGANIC10 applied.")
    else:
        messages.warning(request, "Invalid coupon. Try ORGANIC10.")
    return redirect("cart:detail")


def wishlist_detail(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cart/wishlist.html",
        {"products": services.get_wishlist_products(request)},
    )


@require_POST
def add_wishlist(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id, status=Product.Status.ACTIVE)
    services.add_to_wishlist(request, product)
    messages.success(request, f"{product.name} saved to wishlist.")
    return redirect(request.POST.get("next") or product)


@require_POST
def remove_wishlist(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id, status=Product.Status.ACTIVE)
    services.remove_from_wishlist(request, product)
    messages.info(request, f"{product.name} removed from wishlist.")
    return redirect(request.POST.get("next") or "cart:wishlist")


def checkout(request: HttpRequest) -> HttpResponse:
    summary = services.get_cart_summary(request)
    if not summary.lines:
        messages.info(request, "Your cart is empty. Add products before checkout.")
        return redirect("catalog:product-list")

    if request.method == "POST":
        services.clear_cart(request)
        messages.success(
            request,
            (
                "Order placed successfully. Payment confirmation is ready "
                "for the payment module."
            ),
        )
        return redirect("core:order-success")

    return render(request, "cart/checkout.html", {"summary": summary})
