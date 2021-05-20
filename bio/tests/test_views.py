import pytest
from mixer.backend.django import mixer
from django.test import Client
from engajaflix.settings import AUTH_USER_MODEL
from ..models import SocialLink
pytestmark = pytest.mark.django_db


class TestHomeView:
    view_url = '/bio/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        username = 'test'
        user = mixer.blend(AUTH_USER_MODEL, username=username)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200
        assert username in response.content.decode('utf-8')


class TestLoginView:
    view_url = '/login/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200
        assert '</form>' in response.content.decode('utf-8')

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200
        assert 'logout' in response.content.decode('utf-8')


class TestLogoutView:
    view_url = '/logout/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200


class TestPasswordResetView:
    view_url = '/password/reset/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200
        assert '</form>' in response.content.decode('utf-8')

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200
        assert '</form>' in response.content.decode('utf-8')


class TestPasswordChangeView:
    view_url = '/password/change/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert 'login' in response.url

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200


class TestRegisterView:
    view_url = '/bio/register/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 302

    def test_register_fail(self):
        c = Client()
        response = c.post(self.view_url, data={})
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
        response = c.post(self.view_url, data=body)
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
        response = c.post(self.view_url, data=body)
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
        response = c.post(self.view_url, data=body)
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
        response = c.post(self.view_url, data=body, follow=True)
        assert response.status_code == 200
        assert c.login(username=username, password=password)


class TestProfileView:
    view_url = '/bio/profile/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert 'login' in response.url

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        assert response.status_code == 200

    def test_user_info_in_view(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        user.sociallink_set.add(mixer.blend(SocialLink))
        c.force_login(user)
        response = c.get(self.view_url)
        content = response.content.decode('utf-8')
        print(content)
        assert user.username in content
        if user.picture:
            assert user.picture.url in content
        assert user.first_name in content
        assert user.last_name in content
        if user.pronouns:
            assert user.pronouns in content
        assert user.email in content
        if user.phone:
            assert user.phone in content
        assert user.description in content


