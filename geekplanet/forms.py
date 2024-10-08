from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from geekplanet.models import User, Anime


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
