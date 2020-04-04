"""Simple query string search filter backend."""
import logging

from ...constants import MATCHING_OPTION_MUST
from .base import BaseSearchFilterBackend
from .query_backends import (
    SimpleQueryStringQueryBackend,
)

LOGGER = logging.getLogger(__name__)


__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'simple_query_string'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SimpleQueryStringSearchFilterBackend',
)


class SimpleQueryStringSearchFilterBackend(BaseSearchFilterBackend):
    """Simple query string search filter backend."""

    search_param = 'search_simple_query_string'

    matching = MATCHING_OPTION_MUST

    query_backends = [
        SimpleQueryStringQueryBackend,
    ]
