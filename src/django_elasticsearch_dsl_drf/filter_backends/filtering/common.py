"""
Common filtering backend.
"""

import operator

from elasticsearch_dsl.query import Q
from rest_framework.filters import BaseFilterBackend

import six
from six import string_types

from ...constants import (
    TRUE_VALUES,
    FALSE_VALUES,
    ALL_LOOKUP_FILTERS_AND_QUERIES,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_EXISTS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_STARTSWITH,
    LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_EXCLUDE,
)
from ..mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FilteringFilterBackend',)


class FilteringFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Filtering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     LOOKUP_FILTER_PREFIX,
        >>>     LOOKUP_FILTER_WILDCARD,
        >>>     LOOKUP_QUERY_EXCLUDE,
        >>>     LOOKUP_QUERY_ISNULL,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     FilteringFilterBackend
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
        >>>     filter_backends = [FilteringFilterBackend,]
        >>>     filter_fields = {
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
        filter_fields = view.filter_fields

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
    def get_range_params(cls, value):
        """Get params for `range` query.

        :param value:
        :type: str
        :return: Params to be used in `range` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value, maxsplit=3)
        __len_values = len(__values)

        if __len_values == 0:
            return {}

        params = {
            'gte': __values[0]
        }

        if __len_values == 3:
            params['lte'] = __values[1]
            params['boost'] = __values[2]
        elif __len_values == 2:
            params['lte'] = __values[1]

        return params

    @classmethod
    def get_gte_lte_params(cls, value, lookup):
        """Get params for `gte`, `gt`, `lte` and `lt` query.

        :param value:
        :param lookup:
        :type value: str
        :type lookup: str
        :return: Params to be used in `range` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value, maxsplit=2)
        __len_values = len(__values)

        if __len_values == 0:
            return {}

        params = {
            lookup: __values[0]
        }

        if __len_values == 2:
            params['boost'] = __values[1]

        return params

    @classmethod
    def apply_filter_term(cls, queryset, options, value):
        """Apply `term` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'term',
            **{options['field']: value}
        )

    @classmethod
    def apply_filter_terms(cls, queryset, options, value):
        """Apply `terms` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: mixed: either str or iterable (list, tuple).
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        # If value is a list or a tuple, we use it as is.
        if isinstance(value, (list, tuple)):
            __values = value

        # Otherwise, we consider it to be a string and split it further.
        else:
            __values = cls.split_lookup_value(value)

        return queryset.filter(
            'terms',
            **{options['field']: __values}
        )

    @classmethod
    def apply_filter_range(cls, queryset, options, value):
        """Apply `range` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'range',
            **{options['field']: cls.get_range_params(value)}
        )

    @classmethod
    def apply_query_exists(cls, queryset, options, value):
        """Apply `exists` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        _value_lower = value.lower()
        if _value_lower in TRUE_VALUES:
            return queryset.query(
                Q("exists", field=options['field'])
            )
        elif _value_lower in FALSE_VALUES:
            return queryset.query(
                ~Q("exists", field=options['field'])
            )
        return queryset

    @classmethod
    def apply_filter_prefix(cls, queryset, options, value):
        """Apply `prefix` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'prefix',
            **{options['field']: value}
        )

    @classmethod
    def apply_query_wildcard(cls, queryset, options, value):
        """Apply `wildcard` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q('wildcard', **{options['field']: value})
        )

    @classmethod
    def apply_query_contains(cls, queryset, options, value):
        """Apply `contains` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q('wildcard', **{options['field']: '*{}*'.format(value)})
        )

    @classmethod
    def apply_query_endswith(cls, queryset, options, value):
        """Apply `endswith` filter.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q('wildcard', **{options['field']: '*{}'.format(value)})
        )

    @classmethod
    def apply_query_in(cls, queryset, options, value):
        """Apply `in` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        __values = cls.split_lookup_value(value)
        __queries = []
        for __value in __values:
            __queries.append(
                Q('term', **{options['field']: __value})
            )

        if __queries:
            queryset = queryset.query(
                six.moves.reduce(operator.or_, __queries)
            )

        return queryset

    @classmethod
    def apply_query_gt(cls, queryset, options, value):
        """Apply `gt` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'range',
            **{options['field']: cls.get_gte_lte_params(value, 'gt')}
        )

    @classmethod
    def apply_query_gte(cls, queryset, options, value):
        """Apply `gte` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'range',
            **{options['field']: cls.get_gte_lte_params(value, 'gte')}
        )

    @classmethod
    def apply_query_lt(cls, queryset, options, value):
        """Apply `lt` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'range',
            **{options['field']: cls.get_gte_lte_params(value, 'lt')}
        )

    @classmethod
    def apply_query_lte(cls, queryset, options, value):
        """Apply `lte` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.filter(
            'range',
            **{options['field']: cls.get_gte_lte_params(value, 'lte')}
        )

    @classmethod
    def apply_query_isnull(cls, queryset, options, value):
        """Apply `isnull` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        _value_lower = value.lower()
        if _value_lower in TRUE_VALUES:
            return queryset.query(
                ~Q("exists", field=options['field'])
            )
        elif _value_lower in FALSE_VALUES:
            return queryset.query(
                Q("exists", field=options['field'])
            )
        return queryset

    @classmethod
    def apply_query_exclude(cls, queryset, options, value):
        """Apply `exclude` functional query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        __values = cls.split_lookup_value(value)

        __queries = []
        for __value in __values:
            __queries.append(
                ~Q('term', **{options['field']: __value})
            )

        if __queries:
            queryset = queryset.query(
                six.moves.reduce(operator.or_, __queries)
            )

        return queryset

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
                            'type': view.mapping
                        }
        return filter_query_params

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
        filter_query_params = self.get_filter_query_params(request, view)
        for options in filter_query_params.values():
            # When no specific lookup given, in case of multiple values
            # we apply `terms` filter by default and proceed to the next
            # query param.
            if isinstance(options['values'], (list, tuple)) \
                    and options['lookup'] is None:
                queryset = self.apply_filter_terms(queryset,
                                                   options,
                                                   options['values'])
                continue

            # For all other cases, when we don't have multiple values,
            # we follow the normal flow.
            for value in options['values']:
                # `terms` filter lookup
                if options['lookup'] == LOOKUP_FILTER_TERMS:
                    queryset = self.apply_filter_terms(queryset,
                                                       options,
                                                       value)

                # `prefix` filter lookup
                elif options['lookup'] in (LOOKUP_FILTER_PREFIX,
                                           LOOKUP_QUERY_STARTSWITH):
                    queryset = self.apply_filter_prefix(queryset,
                                                        options,
                                                        value)

                # `range` filter lookup
                elif options['lookup'] == LOOKUP_FILTER_RANGE:
                    queryset = self.apply_filter_range(queryset,
                                                       options,
                                                       value)

                # `exists` filter lookup
                elif options['lookup'] == LOOKUP_FILTER_EXISTS:
                    queryset = self.apply_query_exists(queryset,
                                                       options,
                                                       value)

                # `wildcard` filter lookup
                elif options['lookup'] == LOOKUP_FILTER_WILDCARD:
                    queryset = self.apply_query_wildcard(queryset,
                                                         options,
                                                         value)

                # `contains` filter lookup
                elif options['lookup'] == LOOKUP_QUERY_CONTAINS:
                    queryset = self.apply_query_contains(queryset,
                                                         options,
                                                         value)

                # `in` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_IN:
                    queryset = self.apply_query_in(queryset,
                                                   options,
                                                   value)

                # `gt` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_GT:
                    queryset = self.apply_query_gt(queryset,
                                                   options,
                                                   value)

                # `gte` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_GTE:
                    queryset = self.apply_query_gte(queryset,
                                                    options,
                                                    value)

                # `lt` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_LT:
                    queryset = self.apply_query_lt(queryset,
                                                   options,
                                                   value)

                # `lte` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_LTE:
                    queryset = self.apply_query_lte(queryset,
                                                    options,
                                                    value)

                # `endswith` filter lookup
                elif options['lookup'] == LOOKUP_QUERY_ENDSWITH:
                    queryset = self.apply_query_endswith(queryset,
                                                         options,
                                                         value)

                # `isnull` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_ISNULL:
                    queryset = self.apply_query_isnull(queryset,
                                                       options,
                                                       value)

                # `exclude` functional query lookup
                elif options['lookup'] == LOOKUP_QUERY_EXCLUDE:
                    queryset = self.apply_query_exclude(queryset,
                                                        options,
                                                        value)

                # `term` filter lookup
                else:
                    queryset = self.apply_filter_term(queryset,
                                                      options,
                                                      value)
        return queryset
