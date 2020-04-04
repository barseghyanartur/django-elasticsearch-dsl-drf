"""
Suggester filtering backends.
"""

from .functional import FunctionalSuggesterFilterBackend
from .native import SuggesterFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.suggester'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SuggesterFilterBackend',
    'FunctionalSuggesterFilterBackend',
)
