from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
    UserChangeForm,
    ReadOnlyPasswordHashField,
)
from phonenumber_field.formfields import PhoneNumberField
from django import forms


from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
        field_classes = {
            'username': UsernameField,
            'email': forms.EmailField
        }
