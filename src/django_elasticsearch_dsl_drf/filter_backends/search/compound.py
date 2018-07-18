"""Compound search backend."""

from .base import BaseSearchFilterBackend
from .query_backends import (
    MatchQueryBackend,
    NestedQueryBackend,
)

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.compound'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'CompoundSearchFilterBackend',
)


class CompoundSearchFilterBackend(BaseSearchFilterBackend):
    """Compound search backend."""

    query_backends = [
        MatchQueryBackend,
        NestedQueryBackend,
    ]
