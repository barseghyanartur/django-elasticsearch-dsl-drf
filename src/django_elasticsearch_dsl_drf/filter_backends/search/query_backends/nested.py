import operator
import six

from elasticsearch_dsl.query import Q

from .base import BaseSearchQueryBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.nested'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('NestedQueryBackend',)


class NestedQueryBackend(BaseSearchQueryBackend):
    """Nested query backend."""

    query_type = 'nested'

    @classmethod
    def construct_search(cls, request, view, search_backend):
        """Construct search.

        Dictionary key is the GET param name. The path option stands for the
        path in Elasticsearch.

        Type 1:

            search_nested_fields = {
                'country': {
                    'path': 'country',
                    'fields': ['name'],
                },
                'city': {
                    'path': 'country.city',
                    'fields': ['name'],
                },
            }

        Type 2:

            search_nested_fields = {
                'country': {
                    'path': 'country',
                    'fields': [{'name': {'boost': 2}}]
                },
                'city': {
                    'path': 'country.city',
                    'fields': [{'name': {'boost': 2}}]
                },
            }

        :param request:
        :param view:
        :param search_backend:
        :return:
        """
        if not hasattr(view, 'search_nested_fields'):
            return []

        query_params = search_backend.get_search_query_params(request)
        __queries = []

        for search_term in query_params:
            __values = search_backend.split_lookup_name(search_term, 1)
            __len_values = len(__values)
            if __len_values > 1:
                label, value = __values
                if label in view.search_nested_fields:
                    options = view.search_nested_fields.get(label)
                    path = options.get('path')

                    queries = []
                    for _field in options.get('fields', []):
                        # In case if we deal with structure 2
                        if isinstance(_field, dict):
                            # take options (ex: boost) into consideration
                            field_options = {key: value for key, value in _field.items() if key != 'name'}
                            field_options.update({
                                "query": search_term,
                            })
                            field = "{}.{}".format(path, _field['name'])
                            field_kwargs = {
                                field: field_options,
                            }
                        # In case if we deal with structure 1
                        else:
                            field = "{}.{}".format(path, _field)
                            field_kwargs = {
                                field: value
                            }

                        queries = [
                            Q("match", **field_kwargs)
                        ]

                    __queries.append(
                        Q(
                            cls.query_type,
                            path=path,
                            query=six.moves.reduce(operator.or_, queries)
                        )
                    )
            else:
                for label, options in view.search_nested_fields.items():
                    queries = []
                    path = options.get('path')

                    for _field in options.get('fields', []):
                        # In case if we deal with structure 2
                        if isinstance(_field, dict):
                            # take options (ex: boost) into consideration
                            field_options = {key: value for key, value in _field.items() if key != 'name'}
                            field_options.update({
                                "query": search_term,
                            })
                            field = "{}.{}".format(path, _field['name'])
                            field_kwargs = {
                                field: field_options,
                            }
                        # In case if we deal with structure 1
                        else:
                            field = "{}.{}".format(path, _field)
                            field_kwargs = {
                                field: search_term
                            }

                        queries.append(
                            Q("match", **field_kwargs)
                        )

                    __queries.append(
                        Q(
                            cls.query_type,
                            path=path,
                            query=six.moves.reduce(operator.or_, queries)
                        )
                    )

        return __queries
