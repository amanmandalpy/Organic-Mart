"""Public foundation routes."""

from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sell/", views.sell_center, name="sell-center"),
    path("orders/success/", views.order_success, name="order-success"),
    path("health/live/", views.health_live, name="health-live"),
    path("health/ready/", views.health_ready, name="health-ready"),
]
