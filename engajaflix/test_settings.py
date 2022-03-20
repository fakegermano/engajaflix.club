import secrets
from .settings import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECURE_SSL_REDIRECT = False
LANGUAGE_CODE = 'en-us'
SECRET_KEY = secrets.token_urlsafe()

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
