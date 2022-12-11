try:
    from .base import *
except ImportError:
    pass

DEBUG = True
ALLOWED_HOSTS = ['sokoni.herokuapp.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'socco'
AWS_S3_FILE_OVERIDE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


#STATICFILES_DIRS = [
   # os.path.join(BASE_DIR, 'static'),
#]
#STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




#MPESA_ENVIRONMENT = 'production'

# Credentials for the daraja app

#MPESA_CONSUMER_KEY = env('MPESA_CONSUMER_KEY')
#MPESA_CONSUMER_SECRET = env('MPESA_CONSUMER_SECRET')

#Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

#MPESA_SHORTCODE = '6118954'

# Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# This is only used on sandbox, do not set this variable in production
# For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

#MPESA_EXPRESS_SHORTCODE = '174379'

# Type of shortcode
# Possible values:
# - paybill (For Paybill)
# - till_number (For Buy Goods Till Number)

#MPESA_SHORTCODE_TYPE = 'till_number'

# Lipa na MPESA Online passkey
# Sandbox passkey is available on test credentials page
# Production passkey is sent via email once you go live

#MPESA_PASSKEY = env('MPESA_PASSKEY')
# Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

#MPESA_INITIATOR_USERNAME = env('MPESA_INITIATOR_USERNAME')

# Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

#MPESA_INITIATOR_SECURITY_CREDENTIAL = env('MPESA_INITIATOR_SECURITY_CREDENTIAL')
