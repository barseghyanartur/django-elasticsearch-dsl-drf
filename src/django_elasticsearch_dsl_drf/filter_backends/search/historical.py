"""
Search backend. Most likely to be deprecated soon.
"""

import operator
import warnings

from django_elasticsearch_dsl import fields
from elasticsearch_dsl.query import Q
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings
import six

from ..mixins import FilterBackendMixin
from ...compat import coreapi, coreschema

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.historical'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SearchFilterBackend',)


class SearchFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Search filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     SearchFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.viewsets import (
        >>>     BaseDocumentViewSet,
        >>> )
        >>>
        >>> # Local article document definition
        >>> from .documents import ArticleDocument
        >>>
        >>> # Local article document serializer
        >>> from .serializers import ArticleDocumentSerializer
        >>>
        >>> class ArticleDocumentView(BaseDocumentViewSet):
        >>>
        >>>     document = ArticleDocument
        >>>     serializer_class = ArticleDocumentSerializer
        >>>     filter_backends = [SearchFilterBackend,]
        >>>     search_fields = (
        >>>         'title',
        >>>         'content',
        >>>     )
        >>>     search_nested_fields = {
        >>>         'state': ['name'],
        >>>         'documents.author': ['title', 'description'],
        >>>     }
    """

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

    def construct_nested_search(self, request, view):
        """Construct nested search.

        We have to deal with two types of structures:

        Type 1:

        >>> search_nested_fields = {
        >>>     'country': {
        >>>         'path': 'country',
        >>>         'fields': ['name'],
        >>>     },
        >>>     'city': {
        >>>         'path': 'country.city',
        >>>         'fields': ['name'],
        >>>     },
        >>> }

        Type 2:

        >>> search_nested_fields = {
        >>>     'country': {
        >>>         'path': 'country',
        >>>         'fields': [{'name': {'boost': 2}}]
        >>>     },
        >>>     'city': {
        >>>         'path': 'country.city',
        >>>         'fields': [{'name': {'boost': 2}}]
        >>>     },
        >>> }

        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        if not hasattr(view, 'search_nested_fields'):
            return []

        # TODO: Support query boosting

        query_params = self.get_search_query_params(request)
        __queries = []
        for search_term in query_params:
            for label, options in view.search_nested_fields.items():
                queries = []
                path = options.get('path')

                for _field in options.get('fields', []):

                    # In case if we deal with structure 2
                    if isinstance(_field, dict):
                        # TODO: take options (such as boost) into consideration
                        field = "{}.{}".format(path, _field['name'])
                    # In case if we deal with structure 1
                    else:
                        field = "{}.{}".format(path, _field)

                    field_kwargs = {
                        field: search_term
                    }

                    queries.append(
                        Q("match", **field_kwargs)
                    )

                __queries.append(
                    Q(
                        "nested",
                        path=path,
                        query=six.moves.reduce(operator.or_, queries)
                    )
                )

        return __queries

    def construct_search(self, request, view):
        """Construct search.

        We have to deal with two types of structures:

        Type 1:

        >>> search_fields = (
        >>>     'title',
        >>>     'description',
        >>>     'summary',
        >>> )

        Type 2:

        >>> search_fields = {
        >>>     'title': {'boost': 2},
        >>>     'description': None,
        >>>     'summary': None,
        >>> }

        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        query_params = self.get_search_query_params(request)
        __queries = []
        for search_term in query_params:
            __values = self.split_lookup_name(search_term, 1)
            __len_values = len(__values)
            if __len_values > 1:
                field, value = __values
                if field in view.search_fields:
                    # Initial kwargs for the match query
                    field_kwargs = {field: {'query': value}}
                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        extra_field_kwargs = view.search_fields[field]
                        if extra_field_kwargs:
                            field_kwargs[field].update(extra_field_kwargs)
                    # The match query
                    __queries.append(
                        Q("match", **field_kwargs)
                    )
            else:
                for field in view.search_fields:
                    # Initial kwargs for the match query
                    field_kwargs = {field: {'query': search_term}}

                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        extra_field_kwargs = view.search_fields[field]
                        if extra_field_kwargs:
                            field_kwargs[field].update(extra_field_kwargs)

                    # The match query
                    __queries.append(
                        Q("match", **field_kwargs)
                    )
        return __queries

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
        warnings.warn(
            "{} is deprecated. Switch to `CompoundSearchFilterBackend`."
            "".format(
                self.__class__.__name__
            )
        )
        __queries = self.construct_search(request, view) + \
            self.construct_nested_search(request, view)

        if __queries:
            queryset = queryset.query('bool', should=__queries)
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
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    description='Search in '
                                '{}.'.format(', '.join(search_fields))
                )
            )
        ]
