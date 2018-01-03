"""
Test serializers.
"""

from __future__ import absolute_import

import datetime

import unittest

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from django_elasticsearch_dsl import DocType, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

import pytest

from ..serializers import DocumentSerializer, Meta
from .base import BaseRestFrameworkTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_serializers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSerializers',
)


@pytest.mark.django_db
class TestSerializers(BaseRestFrameworkTestCase):
    """Test serializers."""

    pytestmark = pytest.mark.django_db

    def _get_user_document(self):
        """Get user document."""
        index = Index('auth_user')

        # See Elasticsearch Indices API reference for available settings
        index.settings(
            number_of_shards=1,
            number_of_replicas=1
        )

        @index.doc_type
        class UserDocument(DocType):
            """For testing purposes."""

            id = fields.IntegerField(attr='id')

            username = StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )

            first_name = StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )

            last_name = StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )

            email = StringField(
                fields={
                    'raw': KeywordField(),
                }
            )

            is_staff = fields.BooleanField()

            is_active = fields.BooleanField()

            date_joined = fields.DateField()

            class Meta(object):
                """Meta options."""

                model = User  # The model associate with this DocType

        return UserDocument

    def _get_user_document_serializer(self,
                                      user_document,
                                      with_document=True,
                                      with_exclude=True):
        """Get user document serializer."""

        class UserDocumentSerializer(DocumentSerializer):
            """For testing purposes."""

            class Meta(object):
                """Meta options."""

                if with_document:
                    document = user_document

                fields = (
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_staff',
                    'is_active',
                    'date_joined',
                )

                if with_exclude:
                    exclude = (
                        'username',
                        'first_name',
                    )

            def update(self, instance, validated_data):
                return True

        return UserDocumentSerializer

    def _test_serializer_mix_fields_and_exclude(self):
        """Test serializer mix of fields and exclude.

        This method is supposed to return ``ImproperlyConfigured``
        exception.

        """
        user_document = self._get_user_document()
        user_document_serializer = self._get_user_document_serializer(
            user_document,
            with_document=True,
            with_exclude=True
        )

        return user_document, user_document_serializer

    def test_serializer_fields_and_exclude(self):
        """Test serializer fields and exclude."""

        self.assertRaises(
            ImproperlyConfigured,
            self._test_serializer_mix_fields_and_exclude
        )

    def _test_serializer_no_document_specified(self):
        """Test serializer no document specified."""
        user_document = self._get_user_document()
        user_document_serializer = self._get_user_document_serializer(
            user_document,
            with_document=False,
            with_exclude=False
        )
        return user_document, user_document_serializer()

    def test_serializer_no_document_specified(self):
        """Test serializer no document specified."""
        self.assertRaises(
            ImproperlyConfigured,
            self._test_serializer_no_document_specified
        )

    def _test_serializer_document_equals_to_none(self):
        """Test serializer document equals to none."""
        user_document_serializer = self._get_user_document_serializer(
            None,
            with_document=True,
            with_exclude=False
        )
        return user_document_serializer()

    def test_serializer_document_equals_to_none(self):
        """Test serializer no document specified."""
        self.assertRaises(
            ImproperlyConfigured,
            self._test_serializer_document_equals_to_none
        )

    def _test_serializer_meta_set_attr(self):
        """Test serializer set attr."""
        user_document = self._get_user_document()
        user_document_serializer = self._get_user_document_serializer(
            user_document,
            with_document=True,
            with_exclude=False
        )
        setattr(user_document_serializer.Meta, 'test_name', 'test_value')

    def test_serializer_meta_set_attr(self):
        """Test serializer set attr."""
        self.assertRaises(
            AttributeError,
            self._test_serializer_meta_set_attr
        )

    def _test_serializer_meta_del_attr(self):
        """Test serializer del attr."""
        user_document = self._get_user_document()
        user_document_serializer = self._get_user_document_serializer(
            user_document,
            with_document=True,
            with_exclude=False
        )
        delattr(user_document_serializer.Meta, 'test_name')

    def test_serializer_meta_del_attr(self):
        """Test serializer set attr."""
        self.assertRaises(
            AttributeError,
            self._test_serializer_meta_del_attr
        )


if __name__ == '__main__':
    unittest.main()
