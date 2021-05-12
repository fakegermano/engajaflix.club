import pytest
from mixer.backend.django import mixer
from django.test import Client
from engajaflix.settings import AUTH_USER_MODEL
pytestmark = pytest.mark.django_db


class TestHomeView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/')
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        username = 'test'
        user = mixer.blend(AUTH_USER_MODEL, username=username)
        c.force_login(user)
        response = c.get('/')
        assert response.status_code == 200
        assert username in str(response.content)


