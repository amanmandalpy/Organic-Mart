"""Storefront catalogue URLs."""

from django.urls import path

from apps.catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("suggestions/", views.search_suggestions, name="search-suggestions"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
]
