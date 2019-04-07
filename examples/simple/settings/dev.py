import logging

from .base import *

# if LOGGING:
#     LOGGING['loggers'].update(
#         {
#             'django.db': {
#                 'handlers': ['console'],
#                 'level': 'DEBUG',
#                 'propagate': False,
#             }
#         }
#     )

es_logger = logging.getLogger('elasticsearch')
es_logger.propagate = False
es_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)
es_logger.addHandler(console_handler)
