from .common import *
import dj_database_url
import raven


AWSS3 = os.environ.get('STORAGE') == 'AWSS3' or DEBUG is False

DEBUG = False
ALLOWED_HOSTS = ['*']

if AWSS3:
    CONFIG_SECRET = os.path.join(ROOT_DIR, '.config')
    CONFIG_SETTINGS_COMMON_FILE = os.path.join(CONFIG_SECRET, 'settings_common.json')

    AWS_ACCESSS_KEY_ID = config['aws']['access_key_id']
    AWS_SECRET_ACCESS_KEY = config['aws']['secret_access_key']
    AWS_STORAGE_BUCKET_NAME = config['aws']['s3_bucket_name']
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

    STATICFILES_STORAGE = 'allOnMap.storages.StaticS3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'allOnMap.storages.MediaS3Boto3Storage'

    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        STATIC_DIR,
    )

    STATIC_URL = 's3.{region}.amazonaws.com/{bucket_name}/'.format(
        region=config['aws']['s3_region'],
        bucket_name=config['aws']['s3_storage_bucket_name']
    )

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
