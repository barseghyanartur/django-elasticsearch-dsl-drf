"""
Faceted search backend.
"""
import copy
from collections import defaultdict

from anysearch.search_dsl import TermsFacet
from anysearch.search_dsl.query import Q

from rest_framework.filters import BaseFilterBackend
from six import string_types, iteritems

from .filtering import FilteringFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.faceted_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2022 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FacetedSearchFilterBackend', 'FacetedFilterSearchFilterBackend')


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


class FacetedFilterSearchFilterBackend(FilteringFilterBackend, FacetedSearchFilterBackend):
    """ Combined faceting and filtering backend similar to elasticsearch-dsl's FacetedSearch class.
    It combines the functionality of FilteringFilterBackend and FacetedSearchFilterBackend to take filters into
    account when creating facets.

    This backend uses the same configuration fields as FilteringFilterBackend and FacetedSearchFilterBackend.
    This backend replaces their functionality and should not be used together with either of those backends.

    Note that to work correctly, the actual elasticsearch field must be the same for a facet and its matching filter.
    For example, if a facet will aggregate on field `state.raw`, then the filter must also filter on `state.raw`,
    and not just `state`.

    When creating a facet, filters for faceted fields other than for the current facet are applied. Filters
    for faceted fields are then applied as post_filters. Filters on non-faceted fields are applied as normal filters.
    """
    def filter_queryset(self, request, queryset, view):
        # the fact that apply_filter is a classmethod means we can't store state on self,
        # so we hitch it onto queryset
        queryset._facets = self.construct_facets(request, view)
        queryset._faceted_fields = set(f['facet']._params['field'] for f in queryset._facets.values())
        queryset._filters = defaultdict(list)

        # apply filters
        queryset = FilteringFilterBackend.filter_queryset(self, request, queryset, view)

        # apply aggregations
        return self.aggregate(request, queryset, view)

    @classmethod
    def apply_filter(cls, queryset, options=None, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        facets = queryset._facets
        faceted_fields = queryset._faceted_fields
        filters = queryset._filters

        # if this field is faceted, then apply it as a post-filter
        if options['field'] in faceted_fields:
            queryset = queryset.post_filter(*args, **kwargs)
        else:
            queryset = queryset.filter(*args, **kwargs)

        filters[options['field']].append(Q(*args, **kwargs))

        # ensure the new queryset object retains the helper variables
        queryset._facets = facets
        queryset._faceted_fields = faceted_fields
        queryset._filters = filters
        return queryset

    def aggregate(self, request, queryset, view):
        facets = queryset._facets
        faceted_fields = queryset._faceted_fields
        filters = queryset._filters

        for field, facet in facets.items():
            agg = facet['facet'].get_aggregation()

            if facet['global']:
                queryset.aggs.bucket(
                    '_filter_' + field,
                    'global'
                ).bucket(field, agg)
                continue

            agg_filter = Q('match_all')
            for f, _filter in filters.items():
                # apply filters for that are applicable for facets other than this one
                if agg.field == f or f not in faceted_fields:
                    continue
                # combine with or
                q = _filter[0]
                for x in _filter[1:]:
                    q = q | x
                agg_filter &= q

            queryset.aggs.bucket(
                '_filter_' + field,
                'filter',
                filter=agg_filter
            ).bucket(field, agg)

        return queryset
