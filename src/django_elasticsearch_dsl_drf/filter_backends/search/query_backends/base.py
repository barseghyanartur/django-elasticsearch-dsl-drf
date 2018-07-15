__title__ = 'django_elasticsearch_dsl_drf.filter_backends.search.' \
            'query_backends.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseSearchQueryBackend',)


class BaseSearchQueryBackend(object):
    """Search query backend."""

    @classmethod
    def construct_search(cls, request, view, search_backend):
        """Construct search.

        :param request:
        :param view:
        :param search_backend:
        :return:
        """
        raise NotImplementedError(
            "You should implement `construct_search` method in your {} class"
            "".format(cls.__name__)
        )
