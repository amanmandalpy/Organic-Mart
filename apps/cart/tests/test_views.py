from http import HTTPStatus

import pytest
from django.urls import reverse

from apps.catalog.models import Category, Product


@pytest.fixture
def cart_product(db):
    category = Category.objects.create(
        name="Honey",
        slug="honey",
        description="Raw honey",
        icon="honey",
        display_order=1,
    )
    product = Product.objects.create(
        category=category,
        name="Forest Honey",
        slug="forest-honey",
        short_description="Raw honey jar",
        description="A raw forest honey jar for daily use.",
        seller_name="Wild Hive",
        price="399.00",
        discount_percent=10,
        stock=10,
        sku="HONEY-001",
        package_size="500 g",
        origin="Coorg",
        organic_certification="Natural Honey Certified",
        benefits="Raw\nNatural",
        ingredients="Forest honey",
        rating_average="4.90",
        rating_count=20,
        is_featured=True,
    )
    return product


@pytest.mark.django_db
def test_add_to_cart_and_render_detail(client, cart_product):
    response = client.post(
        reverse("cart:add", args=[cart_product.pk]),
        {"quantity": 2, "next": reverse("cart:detail")},
        follow=True,
    )

    assert response.status_code == HTTPStatus.OK
    assert cart_product.name in response.content.decode()
    session = client.session
    assert str(cart_product.pk) in session["organicmart_cart"]
    assert session["organicmart_cart"][str(cart_product.pk)] == 2


@pytest.mark.django_db
def test_apply_coupon_and_checkout_clears_cart(client, cart_product):
    client.post(
        reverse("cart:add", args=[cart_product.pk]),
        {"quantity": 1},
    )
    coupon_response = client.post(
        reverse("cart:coupon"),
        {"coupon": "ORGANIC10"},
        follow=True,
    )

    assert coupon_response.status_code == HTTPStatus.OK
    assert client.session["organicmart_coupon"] == "ORGANIC10"

    checkout_response = client.post(
        reverse("cart:checkout"),
        follow=True,
    )

    assert checkout_response.status_code == HTTPStatus.OK
    assert "Order confirmed" in checkout_response.content.decode()
    assert client.session["organicmart_cart"] == {}


@pytest.mark.django_db
def test_wishlist_add_and_remove(client, cart_product):
    add_response = client.post(
        reverse("cart:wishlist-add", args=[cart_product.pk]),
        {"next": reverse("cart:wishlist")},
        follow=True,
    )
    assert add_response.status_code == HTTPStatus.OK
    assert str(cart_product.pk) in client.session["organicmart_wishlist"]

    remove_response = client.post(
        reverse("cart:wishlist-remove", args=[cart_product.pk]),
        follow=True,
    )
    assert remove_response.status_code == HTTPStatus.OK
    assert str(cart_product.pk) not in client.session["organicmart_wishlist"]
