"""Small, query-free context values available to every template."""

from typing import Any

from django.http import HttpRequest


def site_context(request: HttpRequest) -> dict[str, Any]:
    del request
    return {
        "site_name": "OrganicMart",
        "support_email": "support@organicmart.example",
    }
