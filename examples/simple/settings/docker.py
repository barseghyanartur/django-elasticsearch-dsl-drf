import os
from .base import *

DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_TEMPLATE = True
DEV = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/backend/examples/db/docker.db',
        'USER': 'postgres',
        'PASSWORD': 'test',
        'HOST': '',
        'PORT': '',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/backend/var/'

DEFAULT_FROM_EMAIL = '<no-reply@localhost>'

os.environ.setdefault(
    'DJANGO_ELASTICSEARCH_DSL_DRF_SOURCE_PATH',
    '/backend/src'
)

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch:9200',
        'timeout': 30,
    },
}
OPENSEARCH_DSL = ELASTICSEARCH_DSL
