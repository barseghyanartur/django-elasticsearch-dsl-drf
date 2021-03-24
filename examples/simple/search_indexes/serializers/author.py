from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import AuthorDocument

__all__ = ('AuthorDocumentSimpleSerializer',)


class AuthorDocumentSimpleSerializer(DocumentSerializer):
    """Serializer for the Author document."""

    source = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""

        document = AuthorDocument
        # fields = (
        #     'id',
        #     'name',
        #     'email',
        #     'salutation',
        # )
        exclude = (
            'headshot',
        )
        ignore_fields = (
            'biography',
            'phone_number',
            'website',
        )

    def get_source(self, obj):
        return obj._d_
