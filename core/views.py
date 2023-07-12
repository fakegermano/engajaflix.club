from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .models import EmailReserve, UuidSession
from .forms import EmailReserveForm, EmailUnreserveForm

class HtmxTemplateView(TemplateView):
    template_name: str
    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return [f"partials/{self.template_name}"]
        return [self.template_name]
    
class IndexView(HtmxTemplateView):
    template_name = "index.html"

class ReserveView(HtmxTemplateView):
    template_name = "reserve.html"

class ReserveProcessView(FormView):
    form_class = EmailReserveForm
    template_name = "partials/_reserve.html"
    success_url = reverse_lazy("unreserve_process")

    def form_valid(self, form: EmailReserveForm) -> HttpResponse:
        session = get_object_or_404(UuidSession, uuid=self.request.session.get("uuid"))
        if session.has_email_reserve:
            reserve = session.email_reserve
        else:
            reserve = EmailReserve(
                session=session,
            )
        reserve.email = form.cleaned_data.get("email")
        reserve.social = form.cleaned_data.get("social")
        reserve.reserved = True
        reserve.save()
        return super().form_valid(form)

class UnreserveProcessView(FormView):
    form_class = EmailUnreserveForm
    template_name = "partials/_unreserve.html"
    success_url = reverse_lazy("reserve_process")

    def form_valid(self, form: EmailUnreserveForm) -> HttpResponse:
        if form.cleaned_data.get("confirm"):
            session = get_object_or_404(UuidSession, uuid=self.request.session.get("uuid"))
            if session.has_email_reserve:
                session.email_reserve.reserved = False
                session.email_reserve.save()
                return super().form_valid(form)
        form.add_error(None, _("algo deu errado, tente novamente mais tarde"))
        return super().form_invalid(form)

index = IndexView.as_view()
reserve = ReserveView.as_view()
reserve_process = ReserveProcessView.as_view()
unreserve_process = UnreserveProcessView.as_view()