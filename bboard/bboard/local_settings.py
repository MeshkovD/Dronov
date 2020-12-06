import os
from pathlib import Path


DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '=08ga8t*_top_secret_^=gi&n)@'


ALLOWED_HOSTS = ["127.0.0.1"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'local_db',
        'USER': 'admin',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
