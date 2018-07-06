from .base import *

if LOGGING:
    LOGGING['loggers'].update(
        {
            'django.db': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        }
    )


# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9201',
        'timeout': 30,
    },
}
