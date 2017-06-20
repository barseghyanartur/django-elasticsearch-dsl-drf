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
