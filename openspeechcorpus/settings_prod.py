import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', "db.contraslash.com")
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', "openspeechcorpus")
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', "mysqluser")
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', "mysqluser")
MYSQL_PORT = os.environ.get('MYSQL_PORT', "3306")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE,
        'USER': MYSQL_USERNAME,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT
    }
}


AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', "bucket_name")
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', "3306")
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', "3306")


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

DEFAULT_FILE_STORAGE = 'openspeechcorpus.storages.MediaStorage'
MEDIAFILES_LOCATION = 'openspeechcorpus/media'
AWS_MEDIA_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_S3_CUSTOM_DOMAIN


STATICFILES_STORAGE = 'openspeechcorpus.storages.StaticStorage'
STATICFILES_LOCATION = 'openspeechcorpus/static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
