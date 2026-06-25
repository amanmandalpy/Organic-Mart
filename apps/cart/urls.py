"""Cart and wishlist URLs."""

from django.urls import path

from apps.cart import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<uuid:product_id>/", views.add_to_cart, name="add"),
    path("update/<uuid:product_id>/", views.update_cart, name="update"),
    path("remove/<uuid:product_id>/", views.remove_from_cart, name="remove"),
    path("coupon/", views.apply_coupon_view, name="coupon"),
    path("wishlist/", views.wishlist_detail, name="wishlist"),
    path("wishlist/add/<uuid:product_id>/", views.add_wishlist, name="wishlist-add"),
    path(
        "wishlist/remove/<uuid:product_id>/",
        views.remove_wishlist,
        name="wishlist-remove",
    ),
    path("checkout/", views.checkout, name="checkout"),
]
