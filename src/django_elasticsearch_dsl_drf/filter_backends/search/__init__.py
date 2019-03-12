"""
Search filter backends.
"""

from .base import BaseSearchFilterBackend
from .compound import CompoundSearchFilterBackend
from .historical import SearchFilterBackend
from .multi_match import MultiMatchSearchFilterBackend
from .simple_query_string import SimpleQueryStringSearchFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseSearchFilterBackend',
    'CompoundSearchFilterBackend',
    'MultiMatchSearchFilterBackend',
    'SearchFilterBackend',
    'SimpleQueryStringSearchFilterBackend',
)
