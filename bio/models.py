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

    phone = PhoneNumberField(_('phone'), blank=True, default="")
    picture = models.ImageField(_('picture'), upload_to='profiles/', blank=True, default="default.png")
    type = models.CharField(_('type'), max_length=1, choices=USER_TYPES, default=DOER)
    pronouns = models.CharField(_('pronouns'), max_length=10, blank=True, default="")
    description = models.TextField(_('description'), blank=True, default="")


class SocialLink(models.Model):
    url = models.URLField(_('url'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("social link")
        verbose_name_plural = _("social links")

    def __str__(self):
        return self.url
