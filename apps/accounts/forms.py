"""Forms for customer registration, login, and profile updates."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.accounts.models import User


class BootstrapFormMixin:
    """Apply consistent Bootstrap styling without repeating widget attrs."""

    def _style_fields(self) -> None:
        for field in self.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} form-control".strip()


class CustomerRegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Email address")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["phone_number"].required = False
        self._style_fields()

    def clean_email(self) -> str:
        email = User.objects.normalize_email(self.cleaned_data["email"])
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class EmailAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Email address")

    def __init__(self, request=None, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"

    def clean_username(self) -> str:
        return User.objects.normalize_email(self.cleaned_data["username"])


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._style_fields()
