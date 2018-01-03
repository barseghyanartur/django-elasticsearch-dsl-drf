"""
Suggesters backend.

It's assumed, that fields you're planning to query suggestions for have been
properly indexed using ``fields.CompletionField``.

Example:

    >>> from django_elasticsearch_dsl import DocType, Index, fields
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
    >>> class PublisherDocument(DocType):
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
    >>>     class Meta(object):
    >>>         "Meta options."
    >>>
    >>>         model = Publisher  # The model associate with this DocType
"""

from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
    ALL_SUGGESTERS,
)

from rest_framework.filters import BaseFilterBackend

from six import string_types

from .mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.suggester'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SuggesterFilterBackend',)


class SuggesterFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Suggester filter backend for Elasticsearch.

    Suggestion functionality is exclusive. Once you have queried the
    ``SuggesterFilterBackend``, the latter will transform your current
    search query into suggestion search query (which is very different).
    Therefore, always add it as the very last filter backend.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     SUGGESTER_TERM,
        >>>     SUGGESTER_PHRASE,
        >>>     SUGGESTER_COMPLETION,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     SuggesterFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet
        >>>
        >>> # Local PublisherDocument definition
        >>> from .documents import PublisherDocument
        >>>
        >>> # Local PublisherDocument serializer
        >>> from .serializers import PublisherDocumentSerializer
        >>>
        >>> class PublisherDocumentView(BaseDocumentViewSet):
        >>>
        >>>     document = PublisherDocument
        >>>     serializer_class = PublisherDocumentSerializer
        >>>     filter_backends = [
        >>>         # ...
        >>>         SuggesterFilterBackend,
        >>>     ]
        >>>     # Suggester fields
        >>>     suggester_fields = {
        >>>         'name_suggest': {
        >>>             'field': 'name.suggest',
        >>>             'suggesters': [
        >>>                 SUGGESTER_TERM,
        >>>                 SUGGESTER_PHRASE,
        >>>                 SUGGESTER_COMPLETION,
        >>>             ],
        >>>         },
        >>>         'city_suggest': {
        >>>             'field': 'city.suggest',
        >>>             'suggesters': [
        >>>                 SUGGESTER_COMPLETION,
        >>>             ],
        >>>         },
        >>>         'state_province_suggest': {
        >>>             'field': 'state_province.suggest',
        >>>             'suggesters': [
        >>>                 SUGGESTER_COMPLETION,
        >>>             ],
        >>>         },
        >>>         'country_suggest': {
        >>>             'field': 'country.suggest',
        >>>             'suggesters': [
        >>>                 SUGGESTER_COMPLETION,
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
        filter_fields = view.suggester_fields

        for field, options in filter_fields.items():
            if options is None or isinstance(options, string_types):
                filter_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in filter_fields[field]:
                filter_fields[field]['field'] = field

            if 'suggesters' not in filter_fields[field]:
                filter_fields[field]['suggesters'] = tuple(
                    ALL_SUGGESTERS
                )

        return filter_fields

    @classmethod
    def apply_suggester_term(cls, suggester_name, queryset, options, value):
        """Apply `term` suggester.

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
        return queryset.suggest(
            suggester_name,
            value,
            term={'field': options['field']}
        )

    @classmethod
    def apply_suggester_phrase(cls, suggester_name, queryset, options, value):
        """Apply `phrase` suggester.

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
        return queryset.suggest(
            suggester_name,
            value,
            phrase={'field': options['field']}
        )

    @classmethod
    def apply_suggester_completion(cls,
                                   suggester_name,
                                   queryset,
                                   options,
                                   value):
        """Apply `completion` suggester.

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
        return queryset.suggest(
            suggester_name,
            value,
            completion={'field': options['field']}
        )

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

                if suggester_param is None \
                        or suggester_param in valid_suggesters:
                    values = [
                        __value.strip()
                        for __value
                        in query_params.getlist(query_param)
                        if __value.strip() != ''
                    ]

                    if values:
                        suggester_query_params[query_param] = {
                            'suggester': suggester_param,
                            'values': values,
                            'field': suggester_fields[field_name].get(
                                'field',
                                field_name
                            ),
                            'type': view.mapping
                        }
        return suggester_query_params

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
        if view.action != 'suggest':
            return queryset

        suggester_query_params = self.get_suggester_query_params(request, view)
        for suggester_name, options in suggester_query_params.items():
            # We don't have multiple values here.
            for value in options['values']:
                # `term` suggester
                if options['suggester'] == SUGGESTER_TERM:
                    queryset = self.apply_suggester_term(suggester_name,
                                                         queryset,
                                                         options,
                                                         value)

                # `phrase` suggester
                elif options['suggester'] == SUGGESTER_PHRASE:
                    queryset = self.apply_suggester_phrase(suggester_name,
                                                           queryset,
                                                           options,
                                                           value)

                # `completion` suggester
                elif options['suggester'] == SUGGESTER_COMPLETION:
                    queryset = self.apply_suggester_completion(suggester_name,
                                                               queryset,
                                                               options,
                                                               value)

        return queryset
