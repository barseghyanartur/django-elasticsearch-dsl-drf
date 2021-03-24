"""
Functional suggesters backend.

It's assumed, that fields you're planning to query suggestions for have been
properly indexed using ``fields.CompletionField``.

Example:

    >>> from django_elasticsearch_dsl import Document, Index, fields
    >>>
    >>> from books.models import Publisher
    >>>
    >>> # Name of the Elasticsearch index
    >>> PUBLISHER_INDEX = Index(PUBLISHER_INDEX_NAME)
    >>> # See Elasticsearch Indices API reference for available settings
    >>> PUBLISHER_INDEX.settings(
    >>>     number_of_shards=1,
    >>>     number_of_replicas=1
    >>> )
    >>>
    >>> @PUBLISHER_INDEX.doc_type
    >>> class PublisherDocument(Document):
    >>>     "Publisher Elasticsearch document."
    >>>
    >>>     id = fields.IntegerField(attr='id')
    >>>
    >>>     name = fields.StringField(
    >>>         fields={
    >>>             'raw': fields.StringField(analyzer='keyword'),
    >>>             'suggest': fields.CompletionField(),
    >>>         }
    >>>     )
    >>>
    >>>     info = fields.StringField()
    >>>
    >>>     address = fields.StringField(
    >>>         fields={
    >>>             'raw': fields.StringField(analyzer='keyword')
    >>>         }
    >>>     )
    >>>
    >>>     city = fields.StringField(
    >>>         fields={
    >>>             'raw': fields.StringField(analyzer='keyword'),
    >>>             'suggest': fields.CompletionField(),
    >>>         }
    >>>     )
    >>>
    >>>     state_province = fields.StringField(
    >>>         fields={
    >>>             'raw': fields.StringField(analyzer='keyword'),
    >>>             'suggest': fields.CompletionField(),
    >>>         }
    >>>     )
    >>>
    >>>     country = fields.StringField(
    >>>         fields={
    >>>             'raw': fields.StringField(analyzer='keyword'),
    >>>             'suggest': fields.CompletionField(),
    >>>         }
    >>>     )
    >>>
    >>>     website = fields.StringField()
    >>>
    >>>     class Meta:
    >>>         "Meta options."
    >>>
    >>>         model = Publisher  # The model associate with this Document
"""
from elasticsearch_dsl.search import AggsProxy

from django_elasticsearch_dsl_drf.constants import (
    FUNCTIONAL_SUGGESTER_TERM_MATCH,
    FUNCTIONAL_SUGGESTER_PHRASE_MATCH,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
    FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
    ALL_FUNCTIONAL_SUGGESTERS,
)
from django_elasticsearch_dsl_drf.utils import EmptySearch

from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend

from six import string_types

from ..mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.suggester.' \
            'functional'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FunctionalSuggesterFilterBackend',)


class FunctionalSuggesterFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Suggester filter backend for Elasticsearch.

    Suggestion functionality is exclusive. Once you have queried the
    ``FunctionalSuggesterFilterBackend``, the latter will transform your
    current search query into another search query (altered).
    Therefore, always add it as the very last filter backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
        >>>     FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        >>>     FUNCTIONAL_SUGGESTER_PHRASE_MATCH,
        >>>     FUNCTIONAL_SUGGESTER_PHRASE_MATCH,
        >>>     FUNCTIONAL_SUGGESTER_TERM_MATCH,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     FunctionalSuggesterFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
        >>>
        >>> # Local PublisherDocument definition
        >>> from .documents import PublisherDocument
        >>>
        >>> # Local PublisherDocument serializer
        >>> from .serializers import PublisherDocumentSerializer
        >>>
        >>> class PublisherDocumentView(DocumentViewSet):
        >>>
        >>>     document = PublisherDocument
        >>>     serializer_class = PublisherDocumentSerializer
        >>>     filter_backends = [
        >>>         # ...
        >>>         FunctionalSuggesterFilterBackend,
        >>>     ]
        >>>     # Suggester fields
        >>>     functional_suggester_fields = {
        >>>         'name_suggest': {
        >>>             'field': 'name.suggest',
        >>>             'suggesters': [
        >>>                 FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
        >>>                 FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        >>>             ],
        >>>         },
        >>>         'city_suggest': {
        >>>             'field': 'city.suggest',
        >>>             'suggesters': [
        >>>                 FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        >>>             ],
        >>>         },
        >>>         'state_province_suggest': {
        >>>             'field': 'state_province.suggest',
        >>>             'suggesters': [
        >>>                 FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
        >>>             ],
        >>>         },
        >>>         'country_suggest': {
        >>>             'field': 'country.suggest',
        >>>             'suggesters': [
        >>>                 FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        >>>             ],
        >>>         },
        >>>     }
    """

    @classmethod
    def prepare_suggester_fields(cls, view):
        """Prepare filter fields.

        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Filtering options.
        :rtype: dict
        """
        filter_fields = view.functional_suggester_fields

        for field, options in filter_fields.items():
            if options is None or isinstance(options, string_types):
                filter_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in filter_fields[field]:
                filter_fields[field]['field'] = field

            if 'suggesters' not in filter_fields[field]:
                filter_fields[field]['suggesters'] = tuple(
                    ALL_FUNCTIONAL_SUGGESTERS
                )

        return filter_fields

    # @classmethod
    # def apply_suggester_term(cls, suggester_name, queryset, options, value):
    #     """Apply `term` suggester.
    #
    #     :param suggester_name:
    #     :param queryset: Original queryset.
    #     :param options: Filter options.
    #     :param value: value to filter on.
    #     :type suggester_name: str
    #     :type queryset: elasticsearch_dsl.search.Search
    #     :type options: dict
    #     :type value: str
    #     :return: Modified queryset.
    #     :rtype: elasticsearch_dsl.search.Search
    #     """
    #     return queryset.suggest(
    #         suggester_name,
    #         value,
    #         term={'field': options['field']}
    #     )
    #
    # @classmethod
    # def apply_suggester_phrase(cls,
    #                            suggester_name,
    #                            queryset,
    #                            options,
    #                            value):
    #     """Apply `phrase` suggester.
    #
    #     :param suggester_name:
    #     :param queryset: Original queryset.
    #     :param options: Filter options.
    #     :param value: value to filter on.
    #     :type suggester_name: str
    #     :type queryset: elasticsearch_dsl.search.Search
    #     :type options: dict
    #     :type value: str
    #     :return: Modified queryset.
    #     :rtype: elasticsearch_dsl.search.Search
    #     """
    #     return queryset.suggest(
    #         suggester_name,
    #         value,
    #         phrase={'field': options['field']}
    #     )

    @classmethod
    def apply_query_size(cls, queryset, options):
        """Apply query size.

        :param queryset:
        :param options:
        :return:
        """
        if 'size' in options['options']:
            queryset = queryset.extra(
                from_=options['options'].get('from', 0),
                size=options['options']['size']
            )
        return queryset

    @classmethod
    def apply_suggester_completion_prefix(cls,
                                          suggester_name,
                                          queryset,
                                          options,
                                          value):
        """Apply `completion` suggester prefix.

        This is effective when used with Keyword fields.

        :param suggester_name:
        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type suggester_name: str
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        queryset = queryset.query(
            'prefix',
            **{options['field']: value}
        )
        queryset = cls.apply_query_size(queryset, options)
        return queryset

    @classmethod
    def apply_suggester_completion_match(cls,
                                         suggester_name,
                                         queryset,
                                         options,
                                         value):
        """Apply `completion` suggester match.

        This is effective when used with Ngram fields.

        :param suggester_name:
        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type suggester_name: str
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        queryset = queryset.query(
            'match',
            **{options['field']: value}
        )
        queryset = cls.apply_query_size(queryset, options)
        return queryset

    def get_suggester_query_params(self, request, view):
        """Get query params to be for suggestions.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Request query params to filter on.
        :rtype: dict
        """
        query_params = request.query_params.copy()

        suggester_query_params = {}
        suggester_fields = self.prepare_suggester_fields(view)
        for query_param in query_params:
            query_param_list = self.split_lookup_filter(
                query_param,
                maxsplit=1
            )
            field_name = query_param_list[0]

            if field_name in suggester_fields:
                suggester_param = None
                if len(query_param_list) > 1:
                    suggester_param = query_param_list[1]

                valid_suggesters = suggester_fields[field_name]['suggesters']

                suggester_options = {}

                # If we have default suggester given use it as a default and
                # do not require further suffix specification.
                default_suggester = None
                if 'default_suggester' in suggester_fields[field_name]:
                    default_suggester = \
                        suggester_fields[field_name]['default_suggester']

                if 'options' in suggester_fields[field_name]:
                    suggester_options = suggester_fields[field_name]['options']

                if suggester_param is None \
                        or suggester_param in valid_suggesters:

                    # If we have default suggester given use it as a default
                    # and do not require further suffix specification.
                    if suggester_param is None \
                            and default_suggester is not None:
                        suggester_param = str(default_suggester)

                    values = [
                        __value.strip()
                        for __value
                        in query_params.getlist(query_param)
                        if __value.strip() != ''
                    ]

                    # If specific field given, use that. Otherwise,
                    # fall back to the top level field name.
                    if 'serializer_field' in suggester_fields[field_name]:
                        serializer_field = \
                            suggester_fields[field_name]['serializer_field']
                    else:
                        serializer_field = suggester_fields[field_name].get(
                            'field',
                            field_name
                        )
                        serializer_field = self.extract_field_name(
                            serializer_field
                        )

                    if values:
                        suggester_query_params[query_param] = {
                            'suggester': suggester_param,
                            'values': values,
                            'field': suggester_fields[field_name].get(
                                'field',
                                field_name
                            ),
                            'type': view.mapping,
                            'serializer_field': serializer_field,
                            'options': suggester_options,
                        }
        return suggester_query_params

    def clean_queryset(self, queryset):
        """Clean the queryset.

        - Remove aggregations.
        - Remove highlight.
        - Remove sorting options.

        :param queryset:
        :return:
        """
        queryset.aggs = AggsProxy('')
        queryset._highlight = {}
        queryset._sort = ['_score']
        queryset._functional_suggest = True
        return queryset

    def serialize_queryset(self,
                           queryset,
                           suggester_name,
                           value,
                           serializer_field):
        """Serialize queryset.

        This shall be done here, since we don't want to delegate it to
        pagination.

        :param queryset:
        :param suggester_name:
        :param value:
        :param serializer_field:
        :return:
        """
        result = queryset.execute().to_dict()
        hits = []
        for hit in result['hits']['hits']:
            hit.update({'text': hit['_source'].get(serializer_field)})
            hits.append(hit)

        data = {
            suggester_name: [{
                'text': value,
                'options': hits,
                'length': len(value),
                'offset': 0,
            }],
            '_shards': result['_shards'],
        }
        return data

    def extract_field_name(self, field_name):
        """Extract field name.

        For instance, "name.suggest" or "name.raw" becomes "name".

        :param field_name:
        :type str:
        :return:
        :rtype: str
        """
        return field_name.split('.')[0]

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
        # The ``SuggesterFilterBackend`` filter backend shall be used in
        # the ``suggest`` custom view action/route only. Usages outside of the
        # are ``suggest`` action/route are restricted.
        if view.action != 'functional_suggest':
            return queryset

        # Clean the queryset.
        queryset = self.clean_queryset(queryset)

        suggester_query_params = self.get_suggester_query_params(request, view)

        applied = False  # Indicates whether filter has been applied
        picked_suggester_name = None
        picked_value = None
        picked_serializer_field = None

        for suggester_name, options in suggester_query_params.items():
            # We don't have multiple values here.
            for value in options['values']:
                # `completion` suggester
                if options['suggester'] == \
                        FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX:
                    queryset = self.apply_suggester_completion_prefix(
                        suggester_name,
                        queryset,
                        options,
                        value
                    )
                    applied = True
                    picked_suggester_name = suggester_name
                    picked_value = value
                    picked_serializer_field = options['serializer_field']

                elif options['suggester'] == \
                        FUNCTIONAL_SUGGESTER_COMPLETION_MATCH:
                    queryset = self.apply_suggester_completion_match(
                        suggester_name,
                        queryset,
                        options,
                        value
                    )
                    applied = True
                    picked_suggester_name = suggester_name
                    picked_value = value
                    picked_serializer_field = options['serializer_field']

                # # `term` suggester
                # elif options['suggester'] == SUGGESTER_TERM:
                #     queryset = self.apply_suggester_term(suggester_name,
                #                                          queryset,
                #                                          options,
                #                                          value)
                #
                # # `phrase` suggester
                # elif options['suggester'] == SUGGESTER_PHRASE:
                #     queryset = self.apply_suggester_phrase(suggester_name,
                #                                            queryset,
                #                                            options,
                #                                            value)

        # If no filters have been applied, return empty queryset. This
        # has no affect on other backends, since this only applies to
        # view.action == 'functional_suggest' case.
        if not applied:
            raise ValidationError(detail=None)
            # empty_queryset = EmptySearch()
            # empty_queryset._functional_suggest = True
            # return empty_queryset

        return self.serialize_queryset(
            queryset,
            picked_suggester_name,
            picked_value,
            picked_serializer_field
        )
