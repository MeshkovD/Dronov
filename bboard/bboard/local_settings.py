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

SOCIAL_AUTH_VK_OAUTH2_KEY = '7644574'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'fdFo05etaWohWOcKcM39'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
#      4d7d97a94d7d97a94d7d97a9114d09323744d7d4d7d97a912e72c6f0ddcd6c1b9c04f9c


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
