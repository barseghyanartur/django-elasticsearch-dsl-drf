import copy

from elasticsearch_dsl.query import Q

from .base import BaseSearchQueryBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.simple_query_string'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SimpleQueryStringQueryBackend',)


class SimpleQueryStringQueryBackend(BaseSearchQueryBackend):
    """Simple query string query backend."""

    query_type = 'simple_query_string'

    @classmethod
    def get_field(cls, field, options):
        """Get field.

        :param field:
        :param options:
        :return:
        """
        if not options:
            options = {}

        field_name = options['field'] \
            if 'field' in options \
            else field

        if 'boost' in options:
            return '{}^{}'.format(field_name, options['boost'])
        return field_name

    @classmethod
    def get_query_options(cls, request, view, search_backend):
        query_options = getattr(view, 'simple_query_string_options', {})
        return query_options

    @classmethod
    def construct_search(cls, request, view, search_backend):
        """Construct search.

        In case of multi match, we always look in a group of fields.
        Thus, matching per field is no longer valid use case here. However,
        we might want to have multiple fields enabled for multi match per
        view set, and only search in some of them in specific request.

        Example:

            /search/books/?search_simple_query_string=
                "fried eggs" %2B(eggplant | potato) -frittata
            /search/books/?search_simple_query_string=
                title,summary:"fried eggs" +(eggplant | potato) -frittata

        Note, that multiple searches are not supported (would not raise
        an exception, but would simply take only the first):

            /search/books/?search_simple_query_string=
                title,summary:"fried eggs" +(eggplant | potato) -frittata
                &search_simple_query_string=
                author,publisher="fried eggs" +(eggplant | potato) -frittata

        In the view-set fields shall be defined in a very simple way. The
        only accepted argument would be boost (per field).

        Example 1 (complex):

            simple_query_string_search_fields = {
                'title': {'field': 'title.english', 'boost': 4},
                'summary': {'boost': 2},
                'description': None,
            }

        Example 2 (simple list):

            simple_query_string_search_fields = (
                'title',
                'summary',
                'description',
            )

        Query examples:

            http://localhost:8000/search
                /books-simple-query-string-search-backend
                /?search_simple_query_string=%22Pool%20of%20Tears%22

            http://localhost:8000/search
                /books-simple-query-string-search-backend
                /?search_simple_query_string=%22Pool%20of%20Tears%22
                -considering

        :param request:
        :param view:
        :param search_backend:
        :return:
        """
        if hasattr(view, 'simple_query_string_search_fields'):
            view_search_fields = copy.copy(
                getattr(view, 'simple_query_string_search_fields')
            )
        else:
            view_search_fields = copy.copy(view.search_fields)

        __is_complex = isinstance(view_search_fields, dict)

        # Getting the list of search query params.
        query_params = search_backend.get_search_query_params(request)

        __queries = []
        for search_term in query_params[:1]:
            __values = search_backend.split_lookup_name(search_term, 1)
            __len_values = len(__values)
            __search_term = search_term

            query_fields = []

            # If we're dealing with case like
            # /search/books/?search_multi_match=title,summary:lorem ipsum
            if __len_values > 1:
                _field, value = __values
                __search_term = value
                fields = search_backend.split_lookup_complex_multiple_value(
                    _field
                )
                for field in fields:
                    if field in view_search_fields:
                        if __is_complex:
                            query_fields.append(
                                cls.get_field(field, view_search_fields[field])
                            )
                        else:
                            query_fields.append(field)

            # If it's just a simple search like
            # /search/books/?search_multi_match=lorem ipsum
            # Fields shall be defined in a very simple way.
            else:
                # It's a dict, see example 1 (complex)
                if __is_complex:
                    for field, options in view_search_fields.items():
                        query_fields.append(
                            cls.get_field(field, options)
                        )

                # It's a list, see example 2 (simple)
                else:
                    query_fields = copy.copy(view_search_fields)

            # The multi match query
            __queries.append(
                Q(
                    cls.query_type,
                    query=__search_term,
                    fields=query_fields,
                    **cls.get_query_options(request, view, search_backend)
                )
            )

        return __queries
