"""Multi match search filter backend."""
import logging

from ...constants import MATCHING_OPTION_MUST
from .base import BaseSearchFilterBackend
from .query_backends import (
    MultiMatchQueryBackend,
)

LOGGER = logging.getLogger(__name__)


__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.multi_match'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'MultiMatchSearchFilterBackend',
)


class MultiMatchSearchFilterBackend(BaseSearchFilterBackend):
    """Multi match search filter backend."""

    search_param = 'search_multi_match'

    matching = MATCHING_OPTION_MUST

    query_backends = [
        MultiMatchQueryBackend,
    ]
