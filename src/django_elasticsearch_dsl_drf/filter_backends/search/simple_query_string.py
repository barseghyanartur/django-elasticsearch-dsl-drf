"""Simple query string search filter backend."""
import logging

from django.core.exceptions import ImproperlyConfigured

from ...constants import MATCHING_OPTION_MUST, MATCHING_OPTIONS
from .base import BaseSearchFilterBackend
from .query_backends import (
    SimpleQueryStringQueryBackend,
)

LOGGER = logging.getLogger(__name__)


__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'simple_query_string'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
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

    # def filter_queryset(self, request, queryset, view):
    #     """Filter the queryset.
    #
    #     :param request: Django REST framework request.
    #     :param queryset: Base queryset.
    #     :param view: View.
    #     :type request: rest_framework.request.Request
    #     :type queryset: elasticsearch_dsl.search.Search
    #     :type view: rest_framework.viewsets.ReadOnlyModelViewSet
    #     :return: Updated queryset.
    #     :rtype: elasticsearch_dsl.search.Search
    #     """
    #     if self.matching not in MATCHING_OPTIONS:
    #         raise ImproperlyConfigured(
    #             "Your `matching` value does not match the allowed matching"
    #             "options: {}".format(', '.join(MATCHING_OPTIONS))
    #         )
    #
    #     __queries = []
    #
    #     for query_backend in self._get_query_backends(request, view):
    #         __queries.extend(
    #             query_backend.construct_search(
    #                 request=request,
    #                 view=view,
    #                 search_backend=self
    #             )
    #         )
    #
    #     if __queries:
    #         # LOGGER.debug(
    #         #     six.moves.reduce(operator.or_, __queries).to_dict()
    #         # )
    #
    #         # Multiple multi match queries are not supported. We pick the
    #         # first one only.
    #         queryset = queryset.query(__queries[0])
    #         # queryset = queryset.query(
    #         #     query=six.moves.reduce(operator.or_, __queries)
    #         # )
    #
    #     # LOGGER.debug(queryset.to_dict())
    #
    #     return queryset
