"""
Mixins.
"""

from ..constants import (
    SEPARATOR_LOOKUP_NAME,
    SEPARATOR_LOOKUP_FILTER,
    SEPARATOR_LOOKUP_COMPLEX_VALUE,
    SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE,
)

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.mixins'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FilterBackendMixin',)


class FilterBackendMixin(object):
    """Filter backend mixin."""

    @classmethod
    def split_lookup_name(cls, value, maxsplit=-1):
        """Split lookup value.

        :param value: Value to split.
        :param maxsplit: The `maxsplit` option of `string.split`.
        :type value: str
        :type maxsplit: int
        :return: Lookup value split into a list.
        :rtype: list
        """
        return value.split(SEPARATOR_LOOKUP_NAME, maxsplit)

    @classmethod
    def split_lookup_filter(cls, value, maxsplit=-1):
        """Split lookup filter.

        :param value: Value to split.
        :param maxsplit: The `maxsplit` option of `string.split`.
        :type value: str
        :type maxsplit: int
        :return: Lookup filter split into a list.
        :rtype: list
        """
        return value.split(SEPARATOR_LOOKUP_FILTER, maxsplit)

    @classmethod
    def split_lookup_complex_value(cls, value, maxsplit=-1):
        """Split lookup complex value.

        :param value: Value to split.
        :param maxsplit: The `maxsplit` option of `string.split`.
        :type value: str
        :type maxsplit: int
        :return: Lookup filter split into a list.
        :rtype: list
        """
        return value.split(SEPARATOR_LOOKUP_COMPLEX_VALUE, maxsplit)

    @classmethod
    def split_lookup_complex_multiple_value(cls, value, maxsplit=-1):
        """Split lookup complex multiple value.

        :param value: Value to split.
        :param maxsplit: The `maxsplit` option of `string.split`.
        :type value: str
        :type maxsplit: int
        :return: Lookup filter split into a list.
        :rtype: list
        """
        return value.split(SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE, maxsplit)

    @classmethod
    def apply_filter(cls, queryset, options=None, args=None, kwargs=None):
        """Apply filter.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        return queryset.filter(*args, **kwargs)

    @classmethod
    def apply_query(cls, queryset, options=None, args=None, kwargs=None):
        """Apply query.

        :param queryset:
        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        return queryset.query(*args, **kwargs)
