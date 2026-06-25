"""API v1 route composition."""

from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import APINotFoundAPIView, FoundationStatusAPIView

app_name = "api"

urlpatterns = [
    path("", FoundationStatusAPIView.as_view(), name="status"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    re_path(
        r"^(?P<unmatched_path>.*)$",
        APINotFoundAPIView.as_view(),
        name="not-found",
    ),
]
