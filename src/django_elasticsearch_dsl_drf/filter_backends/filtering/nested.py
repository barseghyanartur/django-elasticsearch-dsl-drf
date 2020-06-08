"""
Nested filtering backend.
"""

from elasticsearch_dsl.query import Q
from django.core.exceptions import ImproperlyConfigured
from django_elasticsearch_dsl import fields

from six import string_types

from ...constants import (
    ALL_LOOKUP_FILTERS_AND_QUERIES,
    LOOKUP_FILTER_TERMS,
)

from ...compat import coreapi
from ...compat import coreschema
from .common import FilteringFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.nested'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('NestedFilteringFilterBackend',)


class NestedFilteringFilterBackend(FilteringFilterBackend):
    """Nested filter backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     LOOKUP_FILTER_TERM,
        >>>     LOOKUP_FILTER_PREFIX,
        >>>     LOOKUP_FILTER_WILDCARD,
        >>>     LOOKUP_QUERY_EXCLUDE,
        >>>     LOOKUP_QUERY_ISNULL,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     NestedFilteringFilterBackend
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
        >>>     filter_backends = [NestedFilteringFilterBackend,]
        >>>     nested_filter_fields = {
        >>>         'country': {
        >>>             'field': 'continent.country.name.raw',
        >>>             'path': 'continent.country',
        >>>             'lookups': [
        >>>                 LOOKUP_FILTER_TERM,
        >>>                 LOOKUP_FILTER_TERMS,
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
        if not hasattr(view, 'nested_filter_fields'):
            raise ImproperlyConfigured(
                "You need to define `nested_filter_fields` in your `{}` view "
                "when using `{}` filter backend."
                "".format(view.__class__.__name__, cls.__name__)
            )

        filter_fields = view.nested_filter_fields

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

    def get_filter_field_nested_path(self, filter_fields, field_name):
        """Get filter field path to be used in nested query.

        :param filter_fields:
        :param field_name:
        :return:
        """
        if 'path' in filter_fields[field_name]:
            return filter_fields[field_name]['path']
        return field_name

    def get_filter_query_params(self, request, view):
        """Get query params to be filtered on.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Request query params to filter on.
        :rtype: dict
        """
        query_params = request.query_params.copy()

        filter_query_params = {}
        filter_fields = self.prepare_filter_fields(view)
        for query_param in query_params:
            query_param_list = self.split_lookup_filter(
                query_param,
                maxsplit=1
            )
            field_name = query_param_list[0]

            if field_name in filter_fields:
                lookup_param = None
                if len(query_param_list) > 1:
                    lookup_param = query_param_list[1]

                valid_lookups = filter_fields[field_name]['lookups']
                nested_path = self.get_filter_field_nested_path(
                    filter_fields,
                    field_name
                )

                if lookup_param is None or lookup_param in valid_lookups:
                    values = [
                        __value.strip()
                        for __value
                        in query_params.getlist(query_param)
                        if __value.strip() != ''
                    ]

                    if values:
                        filter_query_params[query_param] = {
                            'lookup': lookup_param,
                            'values': values,
                            'field': filter_fields[field_name].get(
                                'field',
                                field_name
                            ),
                            'type': view.mapping,
                            'path': nested_path,
                        }
        return filter_query_params

    @classmethod
    def apply_filter(cls, queryset, options=None, args=None, kwargs=None):
        """Apply filter.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        if options is None or 'path' not in options:
            raise ImproperlyConfigured(
                "You should provide an `path` argument in the field options."
            )

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        return queryset.query(
            'nested',
            path=options.get('path'),
            query=Q(*args, **kwargs)
        )

    @classmethod
    def apply_query(cls, queryset, options=None, args=None, kwargs=None):
        """Apply query.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        if options is None:
            raise ImproperlyConfigured(
                "You should provide an `path` argument in the field options."
            )

        path = options.pop('path')

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        return queryset.query(
            'nested',
            path=path,
            query=Q(*args, **kwargs)
        )

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
        filter_fields = getattr(view, 'nested_filter_fields', None)
        document = getattr(view, 'document', None)

        return [] if not filter_fields else [
            coreapi.Field(
                name=field_name,
                required=False,
                location='query',
                schema=self.get_coreschema_field(
                    document._fields.get(field_name)
                )
            )
            for field_name in filter_fields
        ]
