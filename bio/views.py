from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from verify_email.email_handler import send_verification_email

from .models import CustomUser
from .forms import (
    RegisterForm,
    ProfileEditForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomPasswordSetForm,
)


class IndexView(generic.TemplateView):
    template_name = 'bio/index.html'


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordSetForm


class RegisterView(generic.FormView):
    form_class = RegisterForm
    template_name = 'bio/register.html'
    success_url = reverse_lazy('register')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('logout'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        inactive_user = send_verification_email(self.request, form)
        if inactive_user is None:
            form.add_error('username', _('Failed to create user'))
            return super().form_invalid(form)
        context = self.get_context_data()
        context['email'] = inactive_user.email
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    user = None
    template_name = 'bio/profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.user


class ProfileEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = CustomUser
    user = None
    template_name = 'bio/profile_update.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('bio:profile')

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.user

    def form_valid(self, form):
        inactive_user = send_verification_email(self.request, form)
        if inactive_user is None:
            form.add_error('email', _('Failed to create user'))
            return super().form_invalid(form)
        context = self.get_context_data()
        context['email'] = inactive_user.email
        return self.render_to_response(context)


class ComingSoonView(generic.TemplateView):
    template_name = "index.html"
