"""
Ids filtering backend.

Filters documents that only have the provided ids. Note, this query uses the
`_uid` field.

Elastic query:

    {
        "query": {
            "ids": {
                "type": "book_document",
                "values": ["68", "64", "58"]
            }
        }
    }

REST framework request equivalent:

- http://localhost:8000/api/articles/?ids=68__64__58
- http://localhost:8000/api/articles/?ids=68&ids=64&ids=58

Official Elastic docs:

- https://www.elastic.co/guide/en/elasticsearch/reference/current/
  query-dsl-ids-query.html
"""

from rest_framework.filters import BaseFilterBackend

from ..mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.ids'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('IdsFilterBackend',)


class IdsFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Ids filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     IdsFilterBackend
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
        >>>     filter_backends = [IdsFilterBackend]
    """

    ids_query_param = 'ids'

    def get_ids_query_params(self, request):
        """Get search query params.

        :param request: Django REST framework request.
        :type request: rest_framework.request.Request
        :return: List of search query params.
        :rtype: list
        """
        query_params = request.query_params.copy()
        return query_params.getlist(self.ids_query_param, [])

    def get_ids_values(self, request, view):
        """Get ids values for query.

        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        query_params = self.get_ids_query_params(request)
        __ids = []
        for __id in query_params:
            __values = self.split_lookup_complex_value(__id)
            __ids += __values
        return __ids

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
        __ids = self.get_ids_values(request, view)

        if __ids:
            queryset = queryset.query(
                'ids',
                **{'values': __ids, 'type': view.mapping}
            )
        return queryset
