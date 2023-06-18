from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_safe, require_POST

class HtmxRequest(HttpRequest):
    htmx: bool

# Create your views here.
@require_safe
def index(request: HtmxRequest):
    return render(request, "index.html")

@require_POST
def reserve(request: HtmxRequest):
    if request.htmx: 
        return render(request, "partials/_reserve.html", {"reserved": True})