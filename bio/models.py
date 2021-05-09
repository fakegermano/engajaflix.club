from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):
    MASTER = 'M'
    PATRON = 'P'
    DOER = 'D'

    USER_TYPES = [
        (MASTER, _('master')),
        (PATRON, _('patron')),
        (DOER, _('doer'))
    ]
    """
    Extend the base user model from django
    The following fields already come from AbstractUser
    - first_name
    - last_name
    - username
    - email
    - is_staff
    - is_active
    - date_joined
    - password
    - last_login
    """

    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    picture = models.ImageField(_('picture'), upload_to='profiles/', blank=True, null=True)
    type = models.CharField(_('type'), max_length=1, choices=USER_TYPES, default=DOER)


class SocialLink(models.Model):
    url = models.URLField(_('url'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
