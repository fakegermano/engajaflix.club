from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import RegisterForm


class IndexView(generic.TemplateView):
    template_name = 'bio/index.html'


class RegisterView(generic.FormView):
    form_class = RegisterForm
    template_name = 'bio/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('logout'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        result = super(RegisterView, self).form_valid(form)
        user = form.save()
        if user is None:
            form.add_error('username', _('Failed to create user'))
            return super(RegisterView, self).form_invalid(form)
        return result


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
    fields = (
        'pronouns',
        'first_name',
        'last_name',
        'picture',
        'description',
        'phone',
    )
    success_url = reverse_lazy('bio:edit_profile')

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.user
