from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML, Row, Column, Field
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField

from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser


class TextareaField(forms.CharField):
    widget = forms.Textarea


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-authentication-form'
        self.helper.form_class = 'form-login'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('{% load static %}<img class="mb-4 mt-3" src="{% static "bio/logo.png" %}" alt="engajaflix logo" width="203" height="151">'),  # noqa: E501
            HTML('<h1 class="h3 mb-3 fw-normal">%(translate)s</h1>' % {'translate': _("Please sign in")}),
            FloatingField("username", wrapper_class="required"),
            FloatingField("password", wrapper_class="required"),
            FormActions(
                Submit('login', _("Login")),
            ),
            HTML('<a class="mt-5 mb-3 text-muted" href="%(url)s">%(translate)s</a>' % {'url': reverse_lazy('coming_soon'), 'translate': _("Coming Soon")})  # noqa: E501
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-change-form'
        self.helper.form_class = 'form-change-password'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('<h1 class="h3 mb-3 mt-3 fw-normal">%(translate)s</h1>' % {'translate': _("Password change")}),
            FloatingField("old_password", wrapper_class="required"),
            FloatingField("new_password1", wrapper_class="required"),
            FloatingField("new_password2", wrapper_class="required"),
            FormActions(
                Submit('password-change', _("Password change")),
                Button('cancel', _("Cancel"), css_class="btn-warning", onclick="window.history.back()")
            )
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-form'
        self.helper.form_class = 'form-reset-password'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('<h1 class="h3 mb-3 mt-3 fw-normal">%(translate)s</h1>' % {'translate': _("Reset password")}),
            FloatingField("email", wrapper_class="required"),
            FormActions(
                Submit('reset-password', _("Reset password")),
                Button('cancel', _("Cancel"), css_class="btn-warning", onclick="window.history.back()")
            )
        )


class CustomPasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-set-form'
        self.helper.form_class = 'form-set-password'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('<h1 class="h3 mb-3 mt-3 fw-normal">%(translate)s</h1>' % {'translate': _("Set password")}),
            FloatingField("new_password1", wrapper_class="required"),
            FloatingField("new_password2", wrapper_class="required"),
            FormActions(
                Submit('set-password', _("Set password"))
            )
        )


class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'pronouns', 'first_name', 'last_name', 'description', 'picture')
        field_classes = {
            'username': UsernameField,
            'email': forms.EmailField,
            'pronouns': forms.CharField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'description': TextareaField,
            'picture': forms.ImageField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-register-form'
        self.helper.form_class = 'form-register'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('<h1 class="h3 mb-3 mt-3 fw-normal">%(translate)s</h1>' % {'translate': _("Create your account!")}),
            FloatingField('username', required="true", wrapper_class="required"),
            FloatingField('email', required="true", wrapper_class="required"),
            FloatingField('password1', required="true", wrapper_class="required"),
            FloatingField('password2', required="true", wrapper_class="required"),
            Row(
                Column(
                    FloatingField('pronouns')
                ),
                Column(
                    FloatingField('first_name')
                ),
                Column(
                    FloatingField('last_name')
                )
            ),
            FloatingField('description', css_class="rows-3"),
            Field('picture', template="file_input.html", disabled="disabled"),
            FormActions(
                Submit('register', _("Register")),
                Button('cancel', _("Cancel"), css_class="btn-warning", onclick="window.history.back()"),
            )
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'pronouns',
            'first_name',
            'last_name',
            'picture',
            'description',
            'phone',
        )
        field_classes = {
            'username': UsernameField,
            'email': forms.EmailField,
            'pronouns': forms.CharField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'picture': forms.ImageField,
            'description': TextareaField,
            'phone': PhoneNumberField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-profile-form'
        self.helper.form_class = 'form-profile'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            HTML('<h1 class="h3 mb-3 mt-3 fw-normal">%(translate)s</h1>' % {'translate': _("Edit your profile!")}),
            FloatingField('username', readonly="readonly", wrapper_class="required"),
            Row(
                Column(
                    FloatingField('email', wrapper_class="required"),
                ),
                Column(
                    FloatingField('phone'),
                ),
            ),
            Row(
                Column(
                    FloatingField('pronouns')
                ),
                Column(
                    FloatingField('first_name')
                ),
                Column(
                    FloatingField('last_name')
                ),
            ),
            FloatingField('description', css_class="rows-3"),
            Field('picture', template="file_input.html"),
            FormActions(
                Submit('save', _("Save"), css_class="btn-success"),
                Button('change-password', _("Change password"), css_class="btn-outline-info text-dark",
                       onclick="window.location = \"%(url)s\"" % {'url': reverse_lazy('password_change')}),
                Button('cancel', _("Cancel"), css_class="btn-warning", onclick="window.history.back()")
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        try:
            if self.initial['username'] != cleaned_data['username']:
                self.add_error('username', _("You cannot change the username for now."))
        except KeyError:
            pass
        return cleaned_data
