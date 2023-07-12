from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = _("início")
        context["meta_description"] = _("remova o ruído e encontre uma internet mais diversa")
        context["meta_keywords"] = _("inovação, comunicação, tecnologia, internet, " +
                                     "compartilhe informação, fonte confiável, " +
                                     "pesquise, questione, entenda")
        return context
    

class ReserveView(HtmxTemplateView):
    template_name = "reserve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = _("reserva")
        context["meta_description"] = _("receber novidades e acesso adiantado à plataforma")
        context["meta_keywords"] = _("espera, reserva, novidade, acesso, adiantado")
        return context

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