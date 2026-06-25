from http import HTTPStatus

import pytest
from django.urls import reverse

from apps.catalog.models import Category, Product


@pytest.fixture
def catalog_product(db):
    category = Category.objects.create(
        name="Fruits",
        slug="fruits",
        description="Fresh fruit",
        icon="fruit",
        display_order=1,
    )
    product = Product.objects.create(
        category=category,
        name="Organic Apple Box",
        slug="organic-apple-box",
        short_description="Fresh apples",
        description="A sweet and crisp apple box.",
        seller_name="Farm Fresh",
        price="299.00",
        discount_percent=10,
        stock=25,
        sku="APPLE-001",
        package_size="1 kg",
        origin="Shimla",
        organic_certification="Certified Organic",
        benefits="Fresh\nCrisp",
        ingredients="Organic apples",
        rating_average="4.70",
        rating_count=12,
        is_featured=True,
    )
    return product


@pytest.mark.django_db
def test_product_list_renders_products(client, catalog_product):
    response = client.get(reverse("catalog:product-list"))

    assert response.status_code == HTTPStatus.OK
    assert catalog_product.name in response.content.decode()


@pytest.mark.django_db
def test_product_detail_renders(client, catalog_product):
    response = client.get(
        reverse("catalog:product-detail", args=[catalog_product.slug])
    )

    assert response.status_code == HTTPStatus.OK
    assert catalog_product.organic_certification in response.content.decode()


@pytest.mark.django_db
def test_search_suggestions_returns_json(client, catalog_product):
    response = client.get(
        reverse("catalog:search-suggestions"),
        {"q": "apple"},
    )

    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    assert payload["results"][0]["name"] == catalog_product.name
    assert payload["results"][0]["url"] == catalog_product.get_absolute_url()
