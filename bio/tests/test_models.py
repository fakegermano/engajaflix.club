import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db


class TestCustomUser:
    def test_model(self):
        obj = mixer.blend('bio.CustomUser')
        assert obj.pk == 1, "Should create a user instance"


class TestSocialLink:
    def test_model(self):
        obj = mixer.blend('bio.SocialLink')
        assert obj.pk == 1, "Sould create a SocialLink instance"

    def test_str(self):
        url = "https://example.com"
        obj = mixer.blend('bio.SocialLink', url=url)
        assert str(obj) == url