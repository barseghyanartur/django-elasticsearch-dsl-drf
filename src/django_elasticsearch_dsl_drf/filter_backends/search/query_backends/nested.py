import operator
import six

from elasticsearch_dsl.query import Q

from .base import BaseSearchQueryBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.nested'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('NestedQueryBackend',)


class NestedQueryBackend(BaseSearchQueryBackend):
    """Nested query backend."""

    @classmethod
    def construct_search(cls, request, view, search_backend):
        """Construct search.

        :param request:
        :param view:
        :param search_backend:
        :return:
        """
        if not hasattr(view, 'search_nested_fields'):
            return []

        # TODO: Support query boosting

        query_params = search_backend.get_search_query_params(request)
        __queries = []
        for search_term in query_params:
            for path, _fields in view.search_nested_fields.items():
                queries = []
                for field in _fields:
                    field_key = "{}.{}".format(path, field)
                    queries.append(
                        Q("match", **{field_key: search_term})
                    )

                __queries.append(
                    Q(
                        "nested",
                        path=path,
                        query=six.moves.reduce(operator.or_, queries)
                    )
                )

        return __queries
