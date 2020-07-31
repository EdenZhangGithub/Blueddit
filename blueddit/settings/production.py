from .base import *

DEBUG = False

ALLOWED_HOSTS = ['128.199.119.151']


STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blueddit',
        'USER': 'blueddituser',
        'PASSWORD': 'Eden23494649',
        'HOST': 'localhost',
        'PORT': '',
    }
}