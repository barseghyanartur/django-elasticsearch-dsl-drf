"""
Faceted search backend.
"""
import copy
from elasticsearch_dsl import TermsFacet
from elasticsearch_dsl.query import Q

from rest_framework.filters import BaseFilterBackend

from six import string_types, iteritems

__title__ = 'django_elasticsearch_dsl_drf.faceted_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FacetedSearchFilterBackend',)


class FacetedSearchFilterBackend(BaseFilterBackend):
    """Faceted search backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     FacetedSearchFilterBackend
        >>> )
        >>> from elasticsearch_dsl import TermsFacet, DateHistogramFacet
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
        >>>     filter_backends = [FacetedSearchFilterBackend,]
        >>>     faceted_search_fields = {
        >>>         'title': 'title.raw',  # Uses `TermsFacet` by default
        >>>         'state': {
        >>>             'field': 'state.raw',
        >>>             'facet': TermsFacet,
        >>>         },
        >>>         'publisher': {
        >>>             'field': 'publisher.raw',
        >>>             'facet': TermsFacet,
        >>>             'enabled': False,
        >>>         },
        >>>         'date_published': {
        >>>             'field': 'date_published.raw',
        >>>             'facet': DateHistogramFacet,
        >>>             'options': {
        >>>                 'interval': 'month',
        >>>             },
        >>>             'enabled': True,
        >>>         },
        >>>
        >>>     }

    Facets make queries to be more heavy. That's why by default all
    facets are disabled and enabled only explicitly either in the filter
    options (`enabled` set to True) or via query params
    `?facet=state&facet=date_published`.
    """

    faceted_search_param = 'facet'

    @classmethod
    def prepare_faceted_search_fields(cls, view):
        """Prepare faceted search fields.

        Prepares the following structure:

            >>> {
            >>>     'publisher': {
            >>>         'field': 'publisher.raw',
            >>>         'facet': TermsFacet,
            >>>         'enabled': False,
            >>>     }
            >>>     'date_published': {
            >>>         'field': 'date_published.raw',
            >>>         'facet': DateHistogramFacet,
            >>>         'options': {
            >>>             'interval': 'month',
            >>>         },
            >>>         'enabled': True,
            >>>     },
            >>> }

        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Faceted search fields options.
        :rtype: dict
        """
        faceted_search_fields = copy.deepcopy(view.faceted_search_fields)

        for field, options in faceted_search_fields.items():
            if options is None or isinstance(options, string_types):
                faceted_search_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in faceted_search_fields[field]:
                faceted_search_fields[field]['field'] = field

            if 'enabled' not in faceted_search_fields[field]:
                faceted_search_fields[field]['enabled'] = False

            if 'facet' not in faceted_search_fields[field]:
                faceted_search_fields[field]['facet'] = TermsFacet

            if 'options' not in faceted_search_fields[field]:
                faceted_search_fields[field]['options'] = {}

            faceted_search_fields[field]['global'] = \
                faceted_search_fields[field].get('global', False)

        return faceted_search_fields

    def get_faceted_search_query_params(self, request):
        """Get faceted search query params.

        :param request: Django REST framework request.
        :type request: rest_framework.request.Request
        :return: List of search query params.
        :rtype: list
        """
        query_params = request.query_params.copy()
        return query_params.getlist(self.faceted_search_param, [])

    def construct_facets(self, request, view):
        """Construct facets.

        Turns the following structure:

            >>> {
            >>>     'publisher': {
            >>>         'field': 'publisher.raw',
            >>>         'facet': TermsFacet,
            >>>         'enabled': False,
            >>>     }
            >>>     'date_published': {
            >>>         'field': 'date_published',
            >>>         'facet': DateHistogramFacet,
            >>>         'options': {
            >>>             'interval': 'month',
            >>>         },
            >>>         'enabled': True,
            >>>     },
            >>> }

        Into the following structure:

            >>> {
            >>>     'publisher': TermsFacet(field='publisher.raw'),
            >>>     'publishing_frequency': DateHistogramFacet(
            >>>         field='date_published.raw',
            >>>         interval='month'
            >>>     ),
            >>> }
        """
        __facets = {}
        faceted_search_query_params = self.get_faceted_search_query_params(
            request
        )
        faceted_search_fields = self.prepare_faceted_search_fields(view)
        for __field, __options in faceted_search_fields.items():
            if __field in faceted_search_query_params or __options['enabled']:
                __facets.update(
                    {
                        __field: {
                            'facet': faceted_search_fields[__field]['facet'](
                                field=faceted_search_fields[__field]['field'],
                                **faceted_search_fields[__field]['options']
                            ),
                            'global': faceted_search_fields[__field]['global'],
                        }
                    }
                )
        return __facets

    def aggregate(self, request, queryset, view):
        """Aggregate.

        :param request:
        :param queryset:
        :param view:
        :return:
        """
        __facets = self.construct_facets(request, view)
        for __field, __facet in iteritems(__facets):
            agg = __facet['facet'].get_aggregation()
            agg_filter = Q('match_all')

            # TODO: Implement
            # for __filter_field, __filter in iteritems(self._filters):
            #     if __field == __filter_field:
            #         continue
            #     agg_filter &= __filter

            if __facet['global']:
                queryset.aggs.bucket(
                    '_filter_' + __field,
                    'global'
                ).bucket(__field, agg)
            else:
                queryset.aggs.bucket(
                    '_filter_' + __field,
                    'filter',
                    filter=agg_filter
                ).bucket(__field, agg)

        return queryset

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
        return self.aggregate(request, queryset, view)
