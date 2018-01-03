"""
Common fields.
"""

from rest_framework import serializers
from .helpers import to_representation

__title__ = 'django_elasticsearch_dsl_drf.fields.nested_fields'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BooleanField',
    'CharField',
    'DateField',
    'FloatField',
    'IntegerField',
    'IPAddressField',
)


class BooleanField(serializers.BooleanField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(BooleanField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class CharField(serializers.CharField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(CharField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class DateField(serializers.DateField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(DateField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class FloatField(serializers.FloatField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(FloatField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class IntegerField(serializers.IntegerField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(IntegerField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)


class IPAddressField(serializers.IPAddressField):
    """Object field."""

    def get_value(self, dictionary):
        """Get value."""
        value = super(IPAddressField, self).get_value(dictionary)
        return to_representation(value)

    def to_representation(self, value):
        """To representation."""
        return to_representation(value)
