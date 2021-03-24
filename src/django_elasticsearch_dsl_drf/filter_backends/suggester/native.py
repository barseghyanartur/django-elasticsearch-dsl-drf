"""
Suggesters backend.

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
from collections import defaultdict

from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
    ALL_SUGGESTERS,
)

from rest_framework.filters import BaseFilterBackend

from six import string_types

from ..mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.suggester'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
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
        >>> from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
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
    def get_suggester_context(cls, field, suggester_name, request, view):
        """Get suggester context.

        Given the following definition (in ViewSets):

            >>> # Suggester fields
            >>> suggester_fields = {
            >>>     'title_suggest': {
            >>>         'field': 'title.suggest',
            >>>         'default_suggester': SUGGESTER_COMPLETION,
            >>>     },
            >>>     'title_suggest_context': {
            >>>         'field': 'title.suggest_context',
            >>>         'default_suggester': SUGGESTER_COMPLETION,
            >>>         'completion_options': {
            >>>             'filters': {
            >>>                 'title_suggest_tag': 'tag',
            >>>                 'title_suggest_state': 'state',
            >>>                 'title_suggest_publisher': 'publisher',
            >>>             },
            >>>             'size': 10,
            >>>         }
            >>>     },
            >>> }

        http://localhost:8000/search/books-frontend/suggest/?title_suggest_context=M

        When talking about the queries made, we have the following. Multiple
        values per field are combined with OR:

            >>> completion={
            >>>     'field': options['field'],
            >>>     'size': 10,
            >>>     'contexts': {
            >>>         'tag': ['History', 'Drama'],
            >>>     }
            >>> }

        The following works with OR as well, so it seems we have OR only.
        However, the following construction is more handy, since it allows
        us to play with boosting nicely. Also, it allows to provide `prefix`
        param (which in case of the example given below means that suggestions
        shall match both categories with "Child", "Children", "Childrend's").
        Simply put it's treated as `prefix`, rather than `term`.

            >>> completion={
            >>>     'field': options['field'],
            >>>     'size': 10,
            >>>     'contexts': {
            >>>         'tag': [
            >>>             {'context': 'History'},
            >>>             {'context': 'Drama', 'boost': 2},
            >>>             {'context': 'Children', 'prefix': True},
            >>>         ],
            >>>     },
            >>> }

        Sample query for `category` filter:

            /search/books-frontend/suggest/
            ?title_suggest_context=M
            &title_suggest_tag=Art__2.0
            &title_suggest_tag=Documentary__2.0__prefix
            &title_suggest_publisher=Apress

        The query params would be:

            query_params:
            <QueryDict: {
              'title_suggest_context': ['M'],
              'title_suggest_tag': ['Art__2.0', 'Documentary__2.0__prefix'],
              'title_suggest_publisher': ['Apress']
            }>

        Sample query for `geo` filter:

            /search/address/suggest/
            ?street_suggest_context=M
            &street_suggest_loc=43.66__-79.22__2.0__10000km

        The query params would be:

            query_params:
            <QueryDict: {
              'street_suggest_context': ['M'],
              'street_suggest_loc': ['Art__43.66__-79.22__2.0__10000km'],
            }>

        :return:
        """
        contexts = {}
        query_params = request.query_params.copy()

        # Processing `category` filters:
        for query_param, context_field \
                in field['completion_options'].get('category_filters',
                                                   {}).items():
            context_field_query = defaultdict(list)
            for context_field_value in query_params.getlist(query_param, []):
                context_field_value_parts = cls.split_lookup_filter(
                    context_field_value,
                    maxsplit=2
                )
                # Case `&title_suggest_tag=Documentary__2.0__prefix`
                if len(context_field_value_parts) == 3:
                    context_field_query[context_field].append(
                        {
                            'context': context_field_value_parts[0],
                            'boost': context_field_value_parts[1],
                            'prefix': True,
                        }
                    )
                # Case `&title_suggest_tag=Documentary__2.0` or
                # `&title_suggest_tag=Documentary__prefix`.
                elif len(context_field_value_parts) == 2:
                    if context_field_value_parts[1] == 'prefix':
                        context_field_query[context_field].append(
                            {
                                'context': context_field_value_parts[0],
                                'prefix': True,
                            }
                        )
                    else:
                        context_field_query[context_field].append(
                            {
                                'context': context_field_value_parts[0],
                                'boost': context_field_value_parts[1],
                            }
                        )
                # Case `&title_suggest_tag=Documentary`.
                elif len(context_field_value_parts) == 1:
                    context_field_query[context_field].append(
                        {
                            'context': context_field_value_parts[0],
                        }
                    )

            contexts.update(context_field_query)

        # Processing `geo` filters:
        for query_param, context_field \
                in field['completion_options'].get('geo_filters', {}).items():
            context_field_query = defaultdict(list)
            for context_field_value in query_params.getlist(query_param, []):
                context_field_value_parts = cls.split_lookup_filter(
                    context_field_value,
                    maxsplit=3
                )
                # Case `&street_suggest_loc=43.66__-79.22__2.0__10000km`
                if len(context_field_value_parts) == 4:
                    context_field_query[context_field].append(
                        {
                            'context': {
                                'lat': context_field_value_parts[0],
                                'lon': context_field_value_parts[1],
                            },
                            'precision': context_field_value_parts[2],
                            'boost': context_field_value_parts[3],
                        }
                    )
                # Case `&street_suggest_loc=43.66__-79.22__10000km`.
                elif len(context_field_value_parts) == 3:
                    context_field_query[context_field].append(
                        {
                            'context': {
                                'lat': context_field_value_parts[0],
                                'lon': context_field_value_parts[1],
                            },
                            'precision': context_field_value_parts[2],
                        }
                    )
                # Case `&street_suggest_loc=43.66__-79.22`.
                elif len(context_field_value_parts) == 2:
                    context_field_query[context_field].append(
                        {
                            'context': {
                                'lat': context_field_value_parts[0],
                                'lon': context_field_value_parts[1],
                            },
                        }
                    )

            contexts.update(context_field_query)

        return contexts

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
        completion_kwargs = {
            'field': options['field'],
        }
        if 'size' in options:
            completion_kwargs['size'] = options['size']
        if 'contexts' in options:
            completion_kwargs['contexts'] = options['contexts']
        if 'skip_duplicates' in options:
            completion_kwargs['skip_duplicates'] = options['skip_duplicates']
        return queryset.suggest(
            suggester_name,
            value,
            completion=completion_kwargs
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

                # If we have default suggester given use it as a default and
                # do not require further suffix specification.
                default_suggester = None
                if 'default_suggester' in suggester_fields[field_name]:
                    default_suggester = \
                        suggester_fields[field_name]['default_suggester']

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

                    if values:
                        _sf = suggester_fields[field_name]
                        suggester_query_params[query_param] = {
                            'suggester': suggester_param,
                            'values': values,
                            'field': suggester_fields[field_name].get(
                                'field',
                                field_name
                            ),
                            'type': view.mapping,
                        }

                        if 'options' in _sf:
                            if 'size' in _sf['options']:
                                suggester_query_params[query_param].update({
                                    'size': _sf['options']['size']
                                })
                            if 'skip_duplicates' in _sf['options']:
                                suggester_query_params[query_param].update({
                                    'skip_duplicates':
                                        _sf['options']['skip_duplicates']
                                })

                        if (
                            suggester_param == SUGGESTER_COMPLETION
                            and 'completion_options' in _sf
                            and (
                                'category_filters' in _sf['completion_options']
                                or
                                'geo_filters' in _sf['completion_options']
                            )
                        ):
                            suggester_query_params[query_param]['contexts'] = \
                                self.get_suggester_context(
                                    suggester_fields[field_name],
                                    suggester_param,
                                    request,
                                    view
                                )

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
