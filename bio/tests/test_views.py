import pytest
from mixer.backend.django import mixer
from django.test import Client
from engajaflix.settings import AUTH_USER_MODEL
from ..models import SocialLink
from phonenumbers import example_number_for_type, format_number

pytestmark = pytest.mark.django_db


class MustBeLoggedOut:
    view_url = None

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
        assert 'logout' in response.url


class MustBeLoggedIn:
    view_url = None

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


class TestHomeView:
    view_url = '/bio/'

    def test_anonymous(self):
        c = Client()
        response = c.get(self.view_url)
        assert response.status_code == 200

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert user.username in content


class TestLoginView:
    view_url = '/login/'

    def test_form(self):
        c = Client()
        response = c.get(self.view_url)
        assert '</form>' in response.content.decode('utf-8')

    def test_logged_in(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        c.force_login(user)
        response = c.get(self.view_url)
        content = response.content.decode('utf-8')
        assert 'logout' in content


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


class TestPasswordChangeView(MustBeLoggedIn):
    view_url = '/password/change/'


class TestRegisterView(MustBeLoggedOut):
    view_url = '/bio/register/'

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


class TestProfileView(MustBeLoggedIn):
    view_url = '/bio/profile/'

    def test_user_info_in_view(self):
        c = Client()
        user = mixer.blend(AUTH_USER_MODEL)
        user.sociallink_set.add(mixer.blend(SocialLink))
        c.force_login(user)
        response = c.get(self.view_url)
        content = response.content.decode('utf-8')
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


def gen_phones():
    phones = set()
    for i in range(0, 10):
        num = example_number_for_type(region_code=1, num_type=i)
        print(num)
        phones.add(str(format_number(num, 1)))
    return phones


class TestProfileEditView(MustBeLoggedIn):
    view_url = '/bio/profile/edit/'
    PHONES = [
        "+1 206-564-9959",
        "+1 318-857-8882",
        "+93 70 202 9827",
        "+93 77 221 7514",
        "+54 9 3777 73-6034",
        "+54 9 3888 04-1337",
        "+55 16 93263-6194",
        "+55 24 91213-1794",
        "+55 93 7513-7877",
        "+92 364 8372324",
    ]

    def _edit_field(self, field_name):
        c = Client()
        user = mixer.blend(
            AUTH_USER_MODEL,
            first_name=mixer.FAKE,
            last_name=mixer.FAKE,
            pronouns=mixer.RANDOM,
            description=mixer.RANDOM,
            picture=None,
            phone=mixer.RANDOM(*self.PHONES[:5]),
        )
        old = getattr(user, field_name)
        c.force_login(user)
        body = {field_name: getattr(mixer.blend(
            AUTH_USER_MODEL,
            first_name=mixer.FAKE,
            last_name=mixer.FAKE,
            pronouns=mixer.RANDOM,
            description=mixer.RANDOM,
            picture=None,
            phone=mixer.RANDOM(*self.PHONES[5:]),
        ), field_name)}
        response = c.post(self.view_url, data=body, follow=True)
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'invalid' not in content
        assert str(body[field_name]) in content
        assert str(old) not in content

    def _remove_field(self, field_name):
        c = Client()
        user = mixer.blend(
            AUTH_USER_MODEL,
            first_name=mixer.FAKE,
            last_name=mixer.FAKE,
            pronouns=mixer.RANDOM,
            description=mixer.RANDOM,
            picture=None,
            phone=mixer.RANDOM(*self.PHONES),
        )
        c.force_login(user)
        saved = {field_name: getattr(user, field_name)}
        body = {
            field_name: ""
        }
        response = c.post(self.view_url, data=body, follow=True)
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert str(saved[field_name]) not in content

    def test_edit_first_name(self):
        self._edit_field('first_name')

    def test_remove_first_name(self):
        self._remove_field('first_name')

    def test_edit_last_name(self):
        self._edit_field('last_name')

    def test_remove_last_name(self):
        self._remove_field('last_name')

    def test_edit_pronouns(self):
        self._edit_field('pronouns')

    def test_remove_pronouns(self):
        self._remove_field('pronouns')

    def test_edit_description(self):
        self._edit_field('description')

    def test_remove_description(self):
        self._remove_field('description')

    def test_edit_phone(self):
        self._edit_field('phone')

    def test_remove_phone(self):
        self._remove_field('phone')

    def test_edit_picture(self):
        # FIXME: somehow I can't find a way to test this
        # but manual interaction seems to work
        pass

    def test_remove_picture(self):
        # FIXME: somehow I can't find a way to test this
        # but manual interaction seems to work
        pass