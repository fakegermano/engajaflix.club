import logging
from django.http import HttpRequest
from .models import UuidSession

logger = logging.getLogger(__name__)

def session_uuid(request: HttpRequest) -> dict:
    uuid = request.session.get("uuid")
    session_uuid = UuidSession.objects.get(uuid=uuid)
    return {
        "session_uuid": session_uuid
    }

def session_theme(request: HttpRequest) -> dict:
    theme = request.session.get("theme")
    return {
        "theme": theme
    }