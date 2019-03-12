"""
Highlight backend.
"""
from rest_framework.filters import BaseFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.highlight'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HighlightBackend',)


class HighlightBackend(BaseFilterBackend):
    """Highlight backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     HighlightBackend
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
        >>>     filter_backends = [HighlightBackend,]
        >>>     highlight_fields = {
        >>>         'author.name': {
        >>>             'enabled': False,
        >>>             'options': {
        >>>                 'fragment_size': 150,
        >>>                 'number_of_fragments': 3
        >>>             }
        >>>         }
        >>>         'title': {
        >>>             'options': {
        >>>                 'pre_tags' : ["<em>"],
        >>>                 'post_tags' : ["</em>"]
        >>>             },
        >>>             'enabled': True,
        >>>         },
        >>>     }

    Highlight make queries to be more heavy. That's why by default all
    highlights are disabled and enabled only explicitly either in the filter
    options (`enabled` set to True) or via query params
    `?highlight=author.name&highlight=title`.
    """

    highlight_param = 'highlight'

    @classmethod
    def prepare_highlight_fields(cls, view):
        """Prepare faceted search fields.

        Prepares the following structure:

            >>> {
            >>>     'author.name': {
            >>>         'enabled': False,
            >>>         'options': {
            >>>             'fragment_size': 150,
            >>>             'number_of_fragments': 3
            >>>         }
            >>>     }
            >>>     'title': {
            >>>         'options': {
            >>>             'pre_tags' : ["<em>"],
            >>>             'post_tags' : ["</em>"]
            >>>         },
            >>>         'enabled': True,
            >>>     },
            >>> }

        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Highlight fields options.
        :rtype: dict
        """
        highlight_fields = view.highlight_fields

        for field, options in highlight_fields.items():
            if 'enabled' not in highlight_fields[field]:
                highlight_fields[field]['enabled'] = False

            if 'options' not in highlight_fields[field]:
                highlight_fields[field]['options'] = {}

        return highlight_fields

    def get_highlight_query_params(self, request):
        """Get highlight query params.

        :param request: Django REST framework request.
        :type request: rest_framework.request.Request
        :return: List of search query params.
        :rtype: list
        """
        query_params = request.query_params.copy()
        return query_params.getlist(self.highlight_param, [])

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
        highlight_query_params = self.get_highlight_query_params(request)
        highlight_fields = self.prepare_highlight_fields(view)
        for __field, __options in highlight_fields.items():
            if __field in highlight_query_params or __options['enabled']:
                queryset = queryset.highlight(__field, **__options['options'])

        return queryset
