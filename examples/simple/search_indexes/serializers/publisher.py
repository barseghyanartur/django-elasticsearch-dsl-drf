from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import PublisherDocument

__all__ = (
    'PublisherDocumentSerializer',
    'PublisherDocumentSimpleSerializer',
)


class PublisherDocumentSerializer(serializers.Serializer):
    """Serializer for Publisher document."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    state_province = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)
    website = serializers.CharField(read_only=True)
    location = serializers.SerializerMethodField()

    class Meta(object):
        """Meta options."""

        fields = (
            'id',
            'name',
            'address',
            'city',
            'state_province',
            'country',
            'website',
        )

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

    def get_location(self, obj):
        """Represent location value."""
        try:
            return obj.location.to_dict()
        except Exception:
            return {}


class PublisherDocumentSimpleSerializer(DocumentSerializer):
    """Serializer for Publisher document."""

    class Meta(object):
        """Meta options."""

        document = PublisherDocument
        fields = (
            'id',
            'name',
            'address',
            'city',
            'state_province',
            'country',
            'website',
            'location',
        )
