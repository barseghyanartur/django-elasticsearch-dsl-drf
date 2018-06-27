"""
Utils.
"""

import datetime
from elasticsearch_dsl.search import AggsProxy


__title__ = 'django_elasticsearch_dsl_drf.utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DictionaryProxy',
    'EmptySearch',
)


class EmptySearch(object):
    """Empty Search."""

    def __init__(self, *args, **kwargs):
        self.aggs = AggsProxy('')
        self._highlight = {}
        self._sort = []

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])

    def highlight(self, *args, **kwargs):
        return self

    def sort(self, *args, **kwargs):
        return self

    def execute(self, *args, **kwargs):
        return self

    def to_dict(self, *args, **kwargs):
        return {}


class DictionaryProxy(object):
    """Dictionary proxy."""

    def __init__(self, mapping):
        self.__mapping = mapping

    def __getattr__(self, item):
        val = self.__mapping.get(item, None)
        if isinstance(val, datetime.datetime):
            val = val.date()
        return val

    def to_dict(self):
        """To dict.

        :return:
        """
        return self.__mapping
