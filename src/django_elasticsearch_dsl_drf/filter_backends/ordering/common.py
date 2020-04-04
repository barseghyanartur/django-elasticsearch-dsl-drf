"""
Ordering backend.
"""

from six import string_types

from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from ...compat import coreapi
from ...compat import coreschema
from ...compat import nested_sort_entry

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.ordering.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DefaultOrderingFilterBackend',
    'OrderingFilterBackend',
)


class OrderingMixin(object):
    @classmethod
    def prepare_ordering_fields(cls, view):
        """Prepare ordering fields.

        :param view: View.
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering options.
        :rtype: dict
        """
        ordering_fields = view.ordering_fields.copy()
        for field, options in ordering_fields.items():
            if options is None or isinstance(options, string_types):
                ordering_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in ordering_fields[field]:
                ordering_fields[field]['field'] = field
        return ordering_fields

    @classmethod
    def transform_ordering_params(cls, ordering_params, ordering_fields):
        """Transform ordering fields to elasticsearch-dsl Search.sort()
         dictionary parameters.

        :param ordering_params: List of fields to order by.
        :param ordering_fields: Prepared ordering fields
        :type: list of str
        :type: dict
        :return: Ordering parameters.
        :rtype: list
        """
        _ordering_params = []
        for ordering_param in ordering_params:
            key = ordering_param.lstrip('-')
            direction = 'desc' if ordering_param.startswith('-') else 'asc'
            if key in ordering_fields:
                field = ordering_fields[key]
                entry = {
                    field['field']: {
                        'order': direction,
                    }
                }
                if 'path' in field:
                    entry[field['field']].update(
                        nested_sort_entry(field['path']))
                _ordering_params.append(entry)
        return _ordering_params


class OrderingFilterBackend(BaseFilterBackend, OrderingMixin):
    """Ordering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     OrderingFilterBackend
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
        >>>     filter_backends = [OrderingFilterBackend,]
        >>>     ordering_fields = {
        >>>         'id': None,
        >>>         'title': 'title.raw',
        >>>         'date_submitted': 'date_submitted',
        >>>         'continent': {
        >>>             'field': 'continent.name.raw',
        >>>             'path': 'continent',
        >>>         }
        >>>         'country': {
        >>>             'field': 'continent.country.name.raw',
        >>>             'path': 'continent.country',
        >>>         }
        >>>         'city': {
        >>>             'field': 'continent.country.city.name.raw',
        >>>             'path': 'continent.country.city',
        >>>         }
        >>>     }
        >>>     ordering = ('id', 'title',)
    """

    ordering_param = api_settings.ORDERING_PARAM

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
        # ordering_fields is always dict
        ordering_fields = self.prepare_ordering_fields(view)

        # This is no longer needed. If you want to have a fallback, make use
        # of ``DefaultOrderingFilterBackend``.
        # # If no valid ordering params specified, fall back to `view.ordering`
        # if not __ordering_params:
        #     return self.get_default_ordering_params(view)

        return self.transform_ordering_params(ordering_query_params,
                                              ordering_fields)

    # @classmethod
    # def get_default_ordering_params(cls, view):
    #     """Get the default ordering params for the view.
    #
    #     :param view: View.
    #     :type view: rest_framework.viewsets.ReadOnlyModelViewSet
    #     :return: Ordering params to be used for ordering.
    #     :rtype: list
    #     """
    #     ordering = getattr(view, 'ordering', None)
    #     if isinstance(ordering, string_types):
    #         return [ordering]
    #     return ordering

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

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to ' \
                                    'use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to ' \
                                       'use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Ordering',
                    description='Which field from to use when ordering the '
                                'results.'
                )
            )
        ]


class DefaultOrderingFilterBackend(BaseFilterBackend, OrderingMixin):
    """Default ordering filter backend for Elasticsearch.

    Make sure this is your last ordering backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     DefaultOrderingFilterBackend,
        >>>     OrderingFilterBackend
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
        >>>     filter_backends = [
        >>>         DefaultOrderingFilterBackend,
        >>>         OrderingFilterBackend,
        >>>     ]
        >>>     ordering_fields = {
        >>>         'id': None,
        >>>         'title': 'title.raw',
        >>>         'date_submitted': 'date_submitted',
        >>>         'continent': {
        >>>             'field': 'continent.name.raw',
        >>>             'path': 'continent',
        >>>         }
        >>>         'country': {
        >>>             'field': 'continent.country.name.raw',
        >>>             'path': 'continent.country',
        >>>         }
        >>>         'city': {
        >>>             'field': 'continent.country.city.name.raw',
        >>>             'path': 'continent.country.city',
        >>>         }
        >>>     }
        >>>     ordering = 'city'
    """

    ordering_param = api_settings.ORDERING_PARAM

    def get_ordering_query_params(self, request, view):
        """Get ordering query params.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering params to be used for ordering.
        :rtype: list
        """
        query_params = request.query_params.copy()
        ordering_query_params = query_params.getlist(self.ordering_param, [])
        ordering_params_present = False
        # Remove invalid ordering query params
        for query_param in ordering_query_params:
            __key = query_param.lstrip('-')
            if __key in view.ordering_fields:
                ordering_params_present = True
                break

        # If no valid ordering params specified, fall back to `view.ordering`
        if not ordering_params_present:
            return self.get_default_ordering_params(view)

        return {}

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
            ordering = [ordering]
        # For backwards compatibility require
        # default ordering to be keys in ordering_fields not field value
        # in order to be properly transformed
        if ordering is not None \
                and hasattr(view, 'ordering_fields') \
                and view.ordering_fields is not None \
                and all(field.lstrip('-') in view.ordering_fields
                        for field in ordering):
            return cls.transform_ordering_params(
                ordering,
                cls.prepare_ordering_fields(view)
            )
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
