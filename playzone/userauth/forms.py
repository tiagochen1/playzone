from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        self.fields["username"].widget.attrs.update({
            "placeholder": "Nome",
        })

        
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Password",
        })

        
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm Password",
        })

        # Remover textos de ajuda do django
        for field in self.fields.values():
            field.help_text = ""


class CustomPasswordResetForm(PasswordResetForm):
    """Password reset form styled to match the Figma auth screens."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Email",
                "autocomplete": "email",
            }
        ),
    )
