"""Customer-facing account views."""

from typing import ClassVar

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.accounts.forms import (
    CustomerRegistrationForm,
    EmailAuthenticationForm,
    ProfileUpdateForm,
)


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = CustomerRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your OrganicMart account is ready.")
        return redirect("accounts:profile")

    return render(request, "accounts/register.html", {"form": form})


class CustomerLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    template_name = "accounts/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Welcome back to OrganicMart.")
        return super().form_valid(form)


class CustomerLogoutView(LogoutView):
    http_method_names: ClassVar[list[str]] = ["post"]


@login_required
@require_http_methods(["GET", "POST"])
def profile(request: HttpRequest) -> HttpResponse:
    form = ProfileUpdateForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated.")
        return redirect("accounts:profile")

    return render(request, "accounts/profile.html", {"form": form})
