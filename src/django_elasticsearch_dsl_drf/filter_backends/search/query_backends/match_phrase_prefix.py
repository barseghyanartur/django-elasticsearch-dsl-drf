from elasticsearch_dsl.query import Q

from .base import BaseSearchQueryBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.match_phrase_prefix'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('MatchPhrasePrefixQueryBackend',)


class MatchPhrasePrefixQueryBackend(BaseSearchQueryBackend):
    """Match phrase prefix query backend."""

    query_type = 'match_phrase_prefix'

    @classmethod
    def construct_search(cls, request, view, search_backend):
        """Construct search.

        :param request:
        :param view:
        :param search_backend:
        :return:
        """
        query_params = search_backend.get_search_query_params(request)
        __queries = []
        for search_term in query_params:
            __values = search_backend.split_lookup_name(search_term, 1)
            __len_values = len(__values)
            if __len_values > 1:
                field, value = __values
                if field in view.search_fields:
                    # Initial kwargs for the match query
                    field_kwargs = {field: {'query': value}}
                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        extra_field_kwargs = view.search_fields[field]
                        if extra_field_kwargs:
                            field_kwargs[field].update(extra_field_kwargs)
                    # The match query
                    __queries.append(
                        Q(cls.query_type, **field_kwargs)
                    )
            else:
                for field in view.search_fields:
                    # Initial kwargs for the match query
                    field_kwargs = {field: {'query': search_term}}

                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        extra_field_kwargs = view.search_fields[field]
                        if extra_field_kwargs:
                            field_kwargs[field].update(extra_field_kwargs)

                    # The match query
                    __queries.append(
                        Q(cls.query_type, **field_kwargs)
                    )
        return __queries
