# -*- coding: utf-8 -*-
"""
Serializers.
"""

from __future__ import absolute_import, unicode_literals

import copy
from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured

from django_elasticsearch_dsl import fields, DocType

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils.field_mapping import get_field_kwargs

import six


from .fields import (
    BooleanField,
    CharField,
    DateField,
    FloatField,
    GeoPointField,
    GeoShapeField,
    IntegerField,
    IPAddressField,
    ListField,
    NestedField,
    ObjectField,
)
from .helpers import sort_by_list
from .utils import EmptySearch

__title__ = 'django_elasticsearch_dsl_drf.serializers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DocumentSerializer',
    'DocumentSerializerMeta',
    'Meta',
)


class Meta(type):
    """Template for the DocumentSerializerMeta.Meta class."""

    fields = tuple()
    exclude = tuple()
    search_fields = tuple()
    index_classes = tuple()
    serializers = tuple()
    ignore_fields = tuple()
    field_aliases = {}
    field_options = {}
    index_aliases = {}

    def __new__(mcs, name, bases, attrs):
        cls = super(Meta, mcs).__new__(mcs, str(name), bases, attrs)

        if cls.fields and cls.exclude:
            raise ImproperlyConfigured(
                "%s cannot define both 'fields' and 'exclude'." % name
            )

        return cls

    def __setattr__(cls, name, value):
        raise AttributeError("Meta class is immutable.")

    def __delattr__(cls, name):
        raise AttributeError("Meta class is immutable.")


class DocumentSerializerMeta(serializers.SerializerMetaclass):
    """Metaclass for the DocumentSerializer.

    Ensures that all declared subclasses implemented a Meta.
    """

    def __new__(mcs, name, bases, attrs):
        attrs.setdefault("_abstract", False)

        cls = super(DocumentSerializerMeta, mcs).__new__(
            mcs, str(name), bases, attrs
        )

        if getattr(cls, "Meta", None):
            cls.Meta = Meta("Meta", (Meta,), dict(cls.Meta.__dict__))

        elif not cls._abstract:
            raise ImproperlyConfigured(
                "%s must implement a Meta class or have the property "
                "_abstract" % name
            )

        return cls


class DocumentSerializer(
    six.with_metaclass(DocumentSerializerMeta, serializers.Serializer)
):
    """A dynamic DocumentSerializer class."""

    _abstract = True

    _field_mapping = {
        fields.AttachmentField: CharField,  # Removed from Elasticsearch 6.x
        fields.BooleanField: BooleanField,
        fields.ByteField: CharField,  # TODO
        fields.CompletionField: CharField,  # TODO
        fields.DateField: DateField,
        fields.DoubleField: FloatField,
        fields.FloatField: FloatField,
        fields.GeoPointField: GeoPointField,
        fields.GeoShapeField: GeoShapeField,
        fields.IntegerField: IntegerField,
        fields.IpField: IPAddressField,
        fields.LongField: IntegerField,
        fields.NestedField: NestedField,
        fields.ListField: ListField,
        fields.ObjectField: ObjectField,
        fields.ShortField: IntegerField,
        fields.StringField: CharField,  # Removed in Elasticsearch 6.x
        fields.FileField: CharField,  # TODO
    }

    # Elasticsearch 5.x specific fields
    try:
        _field_mapping.update(
            {
                fields.KeywordField: CharField,
                fields.TextField: CharField
            }
        )

    except AttributeError:
        pass

    def __init__(self, instance=None, data=empty, **kwargs):
        super(DocumentSerializer, self).__init__(instance, data, **kwargs)

        if not hasattr(self.Meta, 'document') or self.Meta.document is None:
            raise ImproperlyConfigured(
                "You must set the 'document' attribute on the serializer "
                "Meta class."
            )

        if not issubclass(self.Meta.document, (DocType,)):
            raise ImproperlyConfigured(
                "You must subclass the serializer 'document' from the DocType"
                "class."
            )

        if not self.instance:
            self.instance = EmptySearch()

    @staticmethod
    def _get_default_field_kwargs(model, field_name, field_type):
        """Get default field kwargs.

        Get the required attributes from the model field in order
        to instantiate a REST Framework serializer field.
        """
        kwargs = {}
        if field_name in model._meta.get_fields():
            model_field = model._meta.get_field(field_type)[0]
            kwargs = get_field_kwargs(field_name, model_field)

            # Remove stuff we don't care about!
            delete_attrs = [
                "allow_blank",
                "choices",
                "model_field",
            ]
            for attr in delete_attrs:
                if attr in kwargs:
                    del kwargs[attr]

        return kwargs

    def _get_index_field(self, field_name):
        """Return the correct index field."""
        return field_name

    def _get_index_class_name(self, index_cls):
        """Get index class name.

        Convert index model class to a name suitable for use as a field name
        prefix.
        """
        cls_name = index_cls.__name__
        aliases = self.Meta.index_aliases
        return aliases.get(cls_name, cls_name.split('.')[-1])

    def get_fields(self):
        """Get the required fields for serializing the result."""
        __fields = self.Meta.fields
        exclude = self.Meta.exclude
        ignore_fields = self.Meta.ignore_fields
        document = self.Meta.document
        model = document._doc_type.model
        document_fields = document._doc_type._fields()

        declared_fields = copy.deepcopy(self._declared_fields)
        field_mapping = OrderedDict()

        for field_name, field_type in six.iteritems(document_fields):
            orig_name = field_name[:]

            # Don't use this field if it is in `ignore_fields`
            if orig_name in ignore_fields or field_name in ignore_fields:
                continue
            # When fields to include are decided by `exclude`
            if exclude:
                if orig_name in exclude or field_name in exclude:
                    continue
            # When fields to include are decided by `fields`
            if __fields:
                if orig_name not in __fields and field_name not in __fields:
                    continue

            # Look up the field attributes on the current index model,
            # in order to correctly instantiate the serializer field.

            kwargs = self._get_default_field_kwargs(
                model,
                field_name,
                field_type
            )
            # If field not in the mapping, just skip
            if field_type.__class__ not in self._field_mapping:
                continue

            field_mapping[field_name] = \
                self._field_mapping[field_type.__class__](**kwargs)

        # Add any explicitly declared fields. They *will* override any index
        # fields in case of naming collision!.
        if declared_fields:
            for field_name in declared_fields:
                field_mapping[field_name] = declared_fields[field_name]

        field_mapping = sort_by_list(field_mapping, __fields)
        return field_mapping

    def create(self, validated_data):
        """Create.

        Do nothing.

        :param validated_data:
        :return:
        """

    def update(self, instance, validated_data):
        """Update.

        Do nothing.

        :param instance:
        :param validated_data:
        :return:
        """
