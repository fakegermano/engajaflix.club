import secrets
from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
LANGUAGE_CODE = 'en-us'

SECRET_KEY = secrets.token_urlsafe()

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
