"""
Search backend.
"""

import operator
import six

from elasticsearch_dsl.query import Q
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from .mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SearchFilterBackend',)


class SearchFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Search filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     SearchFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet
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

        query_params = self.get_search_query_params(request)
        __queries = []
        for search_term in query_params:
            for path, fields in view.search_nested_fields.items():
                queries = []
                for field in fields:
                    field_key = "{}.{}".format(path, field)
                    queries.append(
                        Q("match", **{field_key: search_term})
                    )

                __queries.append(
                    Q("nested",
                      path=path,
                      query=six.moves.reduce(operator.or_, queries)
                      )
                )

        return __queries

    def construct_search(self, request, view):
        """Construct search.

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
            __values = self.split_lookup_value(search_term, 1)
            __len_values = len(__values)
            if __len_values > 1:
                field, value = __values
                if field in view.search_fields:
                    __queries.append(
                        Q("match", **{field: value})
                    )
            else:
                for field in view.search_fields:
                    __queries.append(
                        Q("match", **{field: search_term})
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
        __queries = self.construct_search(request, view) + \
            self.construct_nested_search(request, view)

        if __queries:
            queryset = queryset.query('bool', should=__queries)
        return queryset
