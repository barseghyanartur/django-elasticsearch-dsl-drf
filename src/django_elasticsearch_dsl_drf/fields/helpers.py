"""
Helpers.
"""

from elasticsearch_dsl.utils import AttrDict, AttrList

__title__ = 'django_elasticsearch_dsl_drf.fields.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('to_representation',)


def to_representation(value):
    """To representation."""
    if isinstance(value, AttrDict):
        return value.to_dict()
    if isinstance(value, AttrList):
        return list(value)
    return value
