"""
Nested fields.
"""

from rest_framework.serializers import Field

__title__ = 'django_elasticsearch_dsl_drf.fields.nested_fields'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'GeoPointField',
    'NestedField',
    'ObjectField',
)


class ObjectField(Field):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(ObjectField, self).get_value(dictionary)
        return value.to_dict()

    def to_internal_value(self, data):
        """To internal value."""
        return data

    def to_representation(self, value):
        """To representation."""
        return value.to_dict()


class NestedField(ObjectField):
    """Nested field."""


class GeoPointField(ObjectField):
    """Geo point field."""
