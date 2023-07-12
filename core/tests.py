import logging
from django.test import TransactionTestCase, TestCase
from django.urls import reverse
from .models import UuidSession, EmailReserve

logger = logging.getLogger(__name__)
class IndexViewTestCase(TestCase):
    def setUp(self) -> None:        
        self.url = reverse("index")
        return super().setUp()
    
    def test_view_exists(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "index.html")

    def test_view_generates_uuid(self):
        resp = self.client.get(self.url)
        self.assertEqual(str(resp.context["session_uuid"].uuid), self.client.session["uuid"])

    def test_view_starts_not_reserved(self):
        resp = self.client.get(self.url)
        if "session_uuid" in resp.context:
            self.assertFalse(resp.context["session_uuid"].has_email_reserve)


class ReserveViewTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.url = reverse("reserve")
        return super().setUp()
    
    def test_view_exists(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "reserve.html")
    
    def test_view_not_reserved_shows_reserve(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "reserve/new", status_code=200)

    def test_view_reserved_shows_cancel(self):
        session = self.client.session
        uuid_session = UuidSession.objects.create()
        session["uuid"] = str(uuid_session.uuid)
        uuid_session.save()
        session.save()
        reserve = EmailReserve.objects.create(email="test@example.com", session=uuid_session)
        reserve.save()
        resp = self.client.get(self.url)
        self.assertContains(resp, "reserve/delete", status_code=200)