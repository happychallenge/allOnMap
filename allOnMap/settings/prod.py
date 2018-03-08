from .common import *
import dj_database_url
import raven

DEBUG = False
ALLOWED_HOSTS = ['*']

AWSS3 = True

if AWSS3:

    AWS_ACCESS_KEY_ID = 'AKIAJ2VNH6647EY5UFFA'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'usaofpicture'

    STATICFILES_STORAGE = 'simpleMap.storages.StaticS3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'simpleMap.storages.MediaS3Boto3Storage'

else:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [ join(BASE_DIR, 'staticfiles'),]
    STATIC_ROOT = join(BASE_DIR, 'static')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = join(BASE_DIR, 'media')


INSTALLED_APPS += [ 'raven.contrib.django.raven_compat',  'storages',]

RAVEN_CONFIG = {
    'dsn': 'https://2c8ef02323ba4767b6b53998d63c7942:699ae787482c4efd8381f5605ea93fb8@sentry.io/295620',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}

DATABASES = {
    'default': dj_database_url.parse('postgres://pictureonmap:Tjdrb00$$@localhost:5432/pictureonmap')
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
