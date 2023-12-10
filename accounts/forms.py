from django import forms
from .models import CustomUser as User

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    pass


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]
