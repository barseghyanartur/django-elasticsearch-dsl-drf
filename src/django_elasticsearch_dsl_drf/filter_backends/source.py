"""
Source backend.
"""
from rest_framework.filters import BaseFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.source'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SourceBackend',)


class SourceBackend(BaseFilterBackend):
    """Static source backend.

    Example 1 (simple):

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     SourceBackend
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
        >>>     filter_backends = [SourceBackend,]
        >>>     source = ["title"]

    Example 2 (complex):

        >>> # ...
        >>>     source = ["title", "author.*"]

    Example 3 (even more complex):

        >>> # ...
        >>>     source = {
        >>>         "includes": ["title", "author.*"],
        >>>         "excludes": [ "*.description" ]
        >>>     }

    Source can make queries lighter. However, it can break current
    functionality. Use it with caution.
    """

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
        if getattr(view, 'source', None) is not None:
            queryset = queryset.source(view.source)

        return queryset
