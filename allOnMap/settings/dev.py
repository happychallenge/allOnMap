from .common import *
import dj_database_url

DEBUG = True

AWSS3 = False

INTERNAL_IPS = ["127.0.0.1"] # NOTE: djanog_debug_toolbar 용 설정 추가

INSTALLED_APPS = [ 'debug_toolbar', ] + INSTALLED_APPS
MIDDLEWARE = [ 'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE

DATABASES = {
    'default': dj_database_url.parse('postgres://pictureonmap:Tjdrb00$$@localhost:5432/picturemap')
}

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')
STATICFILES_DIRS = (
  join(BASE_DIR, 'staticfiles/'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR,  'media')