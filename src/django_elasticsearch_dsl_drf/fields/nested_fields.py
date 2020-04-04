"""
Nested fields.
"""

from rest_framework.serializers import Field
from .helpers import to_representation

__title__ = 'django_elasticsearch_dsl_drf.fields.nested_fields'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'GeoPointField',
    'GeoShapeField',
    'NestedField',
    'ObjectField',
    'ListField',
)


class ObjectField(Field):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(ObjectField, self).get_value(dictionary)

        return to_representation(value)

    def to_internal_value(self, data):
        """To internal value."""
        return data

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class NestedField(ObjectField):
    """Nested field."""


class GeoPointField(ObjectField):
    """Geo point field."""


class GeoShapeField(ObjectField):
    """Geo shape field."""


class ListField(Field):
    """List field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(ListField, self).get_value(dictionary)
        return to_representation(value)

    def to_internal_value(self, data):
        """To internal value."""
        return data

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)
