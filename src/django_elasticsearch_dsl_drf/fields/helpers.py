"""
Helpers.
"""
from elasticsearch_dsl.utils import AttrDict, AttrList

__title__ = 'django_elasticsearch_dsl_drf.fields.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('to_representation',)


def to_representation(value):
    """To representation."""
    if isinstance(value, AttrDict):
        return value.to_dict()
    if isinstance(value, AttrList):
        _value = [to_representation(__v) for __v in value]
        return _value
        # If approach above doesn't work, replace it with the code below
        # try:
        #     _value = list(value)
        #     json.dumps(_value)
        #     return _value
        # except TypeError:
        #     _value = [to_representation(__v) for __v in value]
        #     return _value
    return value
