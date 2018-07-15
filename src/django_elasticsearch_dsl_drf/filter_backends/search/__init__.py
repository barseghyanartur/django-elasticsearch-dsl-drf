"""
Search backends.
"""

from .base import BaseSearchBackend
from .common import SearchFilterBackend
from .compound import CompoundSearchBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseSearchBackend',
    'CompoundSearchBackend',
    'SearchFilterBackend',
)
