import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '=08ga8t*s17#1f^(hljtgjhg)7xfpud$@d(i*cxd9o^=gi&n)@'

DEBUG = True

ALLOWED_HOSTS = []



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'bboard.data'),
    }
}



STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
