"""Base search backend."""

from django.core.exceptions import ImproperlyConfigured

from django_elasticsearch_dsl import fields
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from ..mixins import FilterBackendMixin
from ...compat import coreapi, coreschema
from ...constants import MATCHING_OPTIONS, DEFAULT_MATCHING_OPTION

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseSearchFilterBackend',
)


class BaseSearchFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Base search filter backend."""

    query_backends = []

    matching = DEFAULT_MATCHING_OPTION

    search_param = api_settings.SEARCH_PARAM

    def get_search_query_params(self, request):
        """Get search query params.

        :param request: Django REST framework request.
        :type request: rest_framework.request.Request
        :return: List of search query params.
        :rtype: list
        """
        query_params = request.query_params.copy()
        return query_params.getlist(self.search_param, [])

    def get_query_backends(self, request, view):
        """Get query backends.

        :return:
        """
        raise NotImplementedError(
            "You should define `get_query_backends` method in your {} class"
            "".format(self.__class__.__name__)
        )

    def _get_query_backends(self, request, view):
        """Get query backends internal.

        :param request:
        :param view:
        :return:
        """
        try:
            return self.get_query_backends(request, view)
        except NotImplementedError as err:
            pass

        if not self.query_backends:
            raise NotImplementedError(
                "Your search backend shall either implement "
                "`get_query_backends` method or define `query_backends`"
                "property."
            )
        return self.query_backends[:]

    def filter_queryset(self, request, queryset, view):
        """Filter the queryset.

        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        if self.matching not in MATCHING_OPTIONS:
            raise ImproperlyConfigured(
                "Your `matching` value does not match the allowed matching"
                "options: {}".format(', '.join(MATCHING_OPTIONS))
            )

        __query_backends = self._get_query_backends(request, view)

        if len(__query_backends) > 1:
            __queries = []
            for query_backend in __query_backends:
                __queries.extend(
                    query_backend.construct_search(
                        request=request,
                        view=view,
                        search_backend=self
                    )
                )

            if __queries:
                queryset = queryset.query(
                    'bool',
                    **{self.matching: __queries}
                )

        elif len(__query_backends) == 1:
            __query = __query_backends[0].construct_search(
                request=request,
                view=view,
                search_backend=self
            )
            queryset = queryset.query('bool', **{self.matching: __query})

        else:
            raise ImproperlyConfigured(
                "Search filter backend shall have at least one query_backend"
                "specified either in `query_backends` property or "
                "`get_query_backends` method. Make appropriate changes to"
                "your {} class".format(self.__class__.__name__)
            )

        return queryset

    def get_coreschema_field(self, field):
        if isinstance(field, fields.IntegerField):
            field_cls = coreschema.Number
        else:
            field_cls = coreschema.String
        return field_cls()

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to ' \
                                    'use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to ' \
                                       'use `get_schema_fields()`'
        search_fields = getattr(view, 'search_fields', None)

        return [] if not search_fields else [
            coreapi.Field(
                name='search',
                required=False,
                location='query',
                schema=coreschema.String(
                    description='Search in '
                                '{}.'.format(', '.join(search_fields))
                )
            )
        ]
