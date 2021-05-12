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


class TestLoginView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/login/')
        assert response.status_code == 200
        assert '</form>' in str(response.content)

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/login/')
        assert response.status_code == 200
        assert 'logout' in str(response.content)


class TestLogoutView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/logout/')
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/logout/')
        assert response.status_code == 200


class TestPasswordResetView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/password/reset/')
        assert response.status_code == 200
        assert '</form>' in str(response.content)

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/password/reset/')
        assert response.status_code == 200
        assert '</form>' in str(response.content)


class TestPasswordChangeView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/password/change/')
        assert 'login' in response.url

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/password/change/')
        assert response.status_code == 200
