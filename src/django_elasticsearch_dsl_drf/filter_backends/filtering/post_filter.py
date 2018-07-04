"""
The ``post_filter`` filtering backend.
"""

from django_elasticsearch_dsl import fields

from six import string_types

from ...compat import coreapi
from ...compat import coreschema
from ...constants import ALL_LOOKUP_FILTERS_AND_QUERIES

from .common import FilteringFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.' \
            'post_filter.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('PostFilterFilteringFilterBackend',)


class PostFilterFilteringFilterBackend(FilteringFilterBackend):
    """The ``post_filter`` filtering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     LOOKUP_FILTER_PREFIX,
        >>>     LOOKUP_FILTER_WILDCARD,
        >>>     LOOKUP_QUERY_EXCLUDE,
        >>>     LOOKUP_QUERY_ISNULL,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     PostFilterFilteringFilterBackend
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
        >>>     filter_backends = [PostFilterFilteringFilterBackend,]
        >>>     post_filter_fields = {
        >>>         'title': 'title.raw',
        >>>         'state': {
        >>>             'field': 'state.raw',
        >>>             'lookups': [
        >>>                 LOOKUP_FILTER_PREFIX,
        >>>                 LOOKUP_FILTER_WILDCARD,
        >>>                 LOOKUP_QUERY_EXCLUDE,
        >>>                 LOOKUP_QUERY_ISNULL,
        >>>             ],
        >>>         }
        >>> }
    """

    @classmethod
    def prepare_filter_fields(cls, view):
        """Prepare filter fields.

        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Filtering options.
        :rtype: dict
        """
        filter_fields = view.post_filter_fields

        for field, options in filter_fields.items():
            if options is None or isinstance(options, string_types):
                filter_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in filter_fields[field]:
                filter_fields[field]['field'] = field

            if 'lookups' not in filter_fields[field]:
                filter_fields[field]['lookups'] = tuple(
                    ALL_LOOKUP_FILTERS_AND_QUERIES
                )

        return filter_fields

    @classmethod
    def apply_filter(cls, queryset, options=None, args=None, kwargs=None):
        """Apply filter.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        return queryset.post_filter(*args, **kwargs)

    @classmethod
    def apply_query(cls, queryset, options=None, args=None, kwargs=None):
        """Apply query.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        return queryset.post_filter(*args, **kwargs)

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
        filter_fields = getattr(view, 'post_filter_fields', None)
        document = getattr(view, 'document', None)

        return [] if not filter_fields else [
            coreapi.Field(
                name=field_name,
                required=False,
                location='query',
                schema=self.get_coreschema_field(
                    document._doc_type._fields().get(field_name)
                )
            )
            for field_name in filter_fields
        ]
