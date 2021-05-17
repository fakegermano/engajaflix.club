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
        assert username in response.content.decode('utf-8')


class TestLoginView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/login/')
        assert response.status_code == 200
        assert '</form>' in response.content.decode('utf-8')

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/login/')
        assert response.status_code == 200
        assert 'logout' in response.content.decode('utf-8')


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
        assert '</form>' in response.content.decode('utf-8')

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/password/reset/')
        assert response.status_code == 200
        assert '</form>' in response.content.decode('utf-8')


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


class TestRegisterView:
    def test_anonymous(self):
        c = Client()
        response = c.get('/register/')
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get('/register/')
        assert response.status_code == 302

    def test_register_fail(self):
        c = Client()
        response = c.post('/register/', data={})
        assert response.status_code == 200
        assert 'invalid' in response.content.decode('utf-8')

    def test_register_password_fail_weak(self):
        c = Client()
        body = {
            'username': 'test',
            'email': 'test@example.com',
            'password1': '12345678',
            'password2': '12345678'
        }
        response = c.post('/register/', data=body)
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'invalid' in content
        assert 'too common' in content

    def test_register_password_missmatch(self):
        from secrets import token_urlsafe
        c = Client()
        password = token_urlsafe(10)
        password2 = password + '1'
        body = {
            'username': 'test',
            'email': 'test@example.com',
            'password1': password,
            'password2': password2
        }
        response = c.post('/register/', data=body)
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'invalid' in content
        assert 'didn’t match' in content

    def test_register_ok(self):
        from secrets import token_urlsafe
        c = Client()
        password = token_urlsafe(10)
        username = 'test'
        body = {
            'username': username,
            'email': 'test@example.com',
            'password1': password,
            'password2': password
        }
        response = c.post('/register/', data=body)
        assert 'login' in response.url

    def test_register_than_login(self):
        from secrets import token_urlsafe
        c = Client()
        password = token_urlsafe(10)
        username = 'test'
        body = {
            'username': username,
            'email': 'test@example.com',
            'password1': password,
            'password2': password
        }
        response = c.post('/register/', data=body, follow=True)
        assert response.status_code == 200
        assert c.login(username=username, password=password)

