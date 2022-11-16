try:
    from .base import *
except ImportError:
    pass

DEBUG = False
ALLOWED_HOSTS = ['www.sokonisoko.com', 'sokonisoko.com']

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'elytteky'
AWS_S3_ENDPOINT_URL = 'https://elytteky.sgp1.digitaloceanspaces.com'

AWS_S3_CUSTOM_DOMAIN = 'spaces.elytte.com/elytteky'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'elytteky'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'