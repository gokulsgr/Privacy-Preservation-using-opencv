
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    first_name = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    last_name= forms.CharField(
        required = True,
        label = 'First name',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    password = forms.CharField(
        required = True,
        label = 'Last name',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    image = forms.ImageField(required=False)