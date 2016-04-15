from apply.settings import *

DEBUG = True

ALLOWED_HOSTS = ['demo.applycentral.net']

STATIC_URL = "http://demo.applycentral.net/static/"

STATIC_ROOT = '/home/deone/webapps/applycentral_demo_static'

MEDIA_ROOT = "/home/deone/webapps/applycentral_media"

MEDIA_URL = "/media/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'applydb_demo',
        'USER': 'applyadmin_demo',
        'PASSWORD': 'applypass_demo',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
