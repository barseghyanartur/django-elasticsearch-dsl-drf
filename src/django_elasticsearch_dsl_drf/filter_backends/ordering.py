from six import string_types

from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.ordering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('OrderingFilterBackend',)


class OrderingFilterBackend(BaseFilterBackend):
    """Ordering filter backend for ElasticSearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     OrderingFilterBackend
        >>> )
        >>> from rest_framework.viewsets import ReadOnlyModelViewSet
        >>>
        >>> # Local article document definition
        >>> from .documents import ArticleDocument
        >>>
        >>> # Local article document serializer
        >>> from .serializers import ArticleDocumentSerializer
        >>>
        >>> class ArticleDocumentView(ReadOnlyModelViewSet):
        >>>
        >>>     document = ArticleDocument
        >>>     serializer_class = ArticleDocumentSerializer
        >>>     filter_backends = [OrderingFilterBackend,]
        >>>     ordering_fields = {
        >>>         'id': 'id',
        >>>         'title': 'title.raw',
        >>>         'date_submitted': 'date_submitted',
        >>>         'state': {
        >>>             'field': 'state.raw',
        >>>         }
        >>>     }
    """

    ordering_param = api_settings.ORDERING_PARAM

    @classmethod
    def prepare_ordering_fields(cls, view):
        """Prepare ordering fields.

        :param view: View.
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering options.
        :rtype: dict
        """
        ordering_fields = view.ordering_fields
        for field, options in ordering_fields.items():
            if options is None or isinstance(options, string_types):
                ordering_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in ordering_fields[field]:
                ordering_fields[field]['field'] = field
        return ordering_fields

    def get_ordering_query_params(self, request, view):
        """Get ordering query params.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering params to be used for ordering.
        :rtype: list
        """
        # TODO: Support `mode` argument.
        query_params = request.query_params.copy()
        ordering_query_params = query_params.getlist(self.ordering_param, [])

        # Remove invalid ordering query params
        for query_param in ordering_query_params:
            __key = query_param.lstrip('-')
            if __key not in view.ordering_fields:
                ordering_query_params.remove(query_param)

        # If no valid ordering params specified, fall back to `view.ordering`
        if not ordering_query_params:
            return self.get_default_ordering_params(view)

        return ordering_query_params

    @classmethod
    def get_default_ordering_params(cls, view):
        """Get the default ordering params for the view.

        :param view: View.
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering params to be used for ordering.
        :rtype: list
        """
        ordering = getattr(view, 'ordering', None)
        if isinstance(ordering, string_types):
            return [ordering]
        return ordering

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
        ordering_query_params = self.get_ordering_query_params(request, view)

        if ordering_query_params:
            return queryset.sort(*ordering_query_params)

        return queryset
