"""
Mixins.
"""

from ..constants import (
    SEPARATOR_LOOKUP_VALUE,
    SEPARATOR_LOOKUP_FILTER,
    SEPARATOR_LOOKUP_COMPLEX_VALUE,
)

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.mixins'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FilterBackendMixin',)


class FilterBackendMixin(object):
    """Filter backend mixin."""

    @classmethod
    def split_lookup_value(cls, value, maxsplit=-1):
        """Split lookup value.

        :param value: Value to split.
        :param maxsplit: The `maxsplit` option of `string.split`.
        :type value: str
        :type maxsplit: int
        :return: Lookup value split into a list.
        :rtype: list
        """
        return value.split(SEPARATOR_LOOKUP_VALUE, maxsplit)

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
