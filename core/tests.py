import logging
from django.test import TestCase
from django.urls import reverse
from .models import UuidSession, EmailReserve

logger = logging.getLogger(__name__)
class IndexViewTestCase(TestCase):
    def setUp(self) -> None:        
        self.url = reverse("index")
        return super().setUp()
    
    def test_view_exists(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "engajaflix", status_code=200, html=True)

    def test_view_generates_uuid(self):
        resp = self.client.get(self.url)
        self.assertEqual(str(resp.context["session_uuid"].uuid), self.client.session["uuid"])

    def test_view_starts_not_reserved(self):
        resp = self.client.get(self.url)
        if "reserved" in resp.context:
            self.assertFalse(resp.context["reserved"])

    def test_view_reserve_session(self):
        uuid_session = UuidSession.objects.create()
        self.client.session["uuid"] = uuid_session.uuid
        uuid_session.save()
        reserve = EmailReserve.objects.create(email="test@example.com", session=uuid_session)
        reserve.save()
        resp = self.client.get(self.url)
        self.assertContains(resp, "Reserve", status_code=200, html=True)