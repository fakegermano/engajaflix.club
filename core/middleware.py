from collections.abc import Callable
from uuid import uuid4
from django.http import HttpRequest, HttpResponse
import logging
from .models import UuidSession

logger = logging.getLogger(__name__)

class UuidMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        uuid = request.session.get("uuid", str(uuid4()))
        session_uuid, created = UuidSession.objects.get_or_create(uuid=uuid)
        if created:
            logger.debug("created new session_uuid")
        if request.user.is_authenticated:
            session_uuid.user = request.user
        session_uuid.save()
        request.session["uuid"] = str(session_uuid.uuid)
        return self.get_response(request)
    
class ThemeMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        theme = request.session.get("theme", "dark")
        request.session["theme"] = theme
        return self.get_response(request)