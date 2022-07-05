from copy import deepcopy

from elasticsearch_dsl.query import Q

from .base import BaseSearchQueryBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.match_phrase'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('MatchPhraseQueryBackend',)


class MatchPhraseQueryBackend(BaseSearchQueryBackend):
    """Match phrase query backend."""

    query_type = 'match_phrase'

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
                    field_kwargs = {}
                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        field_name = deepcopy(field)
                        extra_field_kwargs = deepcopy(view.search_fields[field])
                        if extra_field_kwargs:
                            if "field" in extra_field_kwargs:
                                field_name = extra_field_kwargs.pop("field")
                            # Initial kwargs for the match query
                            field_kwargs = {field_name: {"query": value}}
                            field_kwargs[field_name].update(extra_field_kwargs)

                    if not field_kwargs:
                        field_kwargs = {field: {"query": value}}

                    # The match query
                    __queries.append(
                        Q(cls.query_type, **field_kwargs)
                    )
            else:
                for field in view.search_fields:
                    # Initial kwargs for the match query
                    field_kwargs = {}

                    # In case if we deal with structure 2
                    if isinstance(view.search_fields, dict):
                        field_name = deepcopy(field)
                        extra_field_kwargs = deepcopy(view.search_fields[field])
                        if extra_field_kwargs:
                            if "field" in extra_field_kwargs:
                                field_name = extra_field_kwargs.pop("field")
                            # Initial kwargs for the match query
                            field_kwargs = {field_name: {"query": search_term}}
                            field_kwargs[field_name].update(extra_field_kwargs)

                    if not field_kwargs:
                        field_kwargs = {field: {"query": search_term}}

                    # The match query
                    __queries.append(
                        Q(cls.query_type, **field_kwargs)
                    )
        return __queries
