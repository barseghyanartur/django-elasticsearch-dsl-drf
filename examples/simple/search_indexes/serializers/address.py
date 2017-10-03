from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import AddressDocument

__all__ = ('AddressDocumentSerializer',)


class AddressDocumentSerializer(DocumentSerializer):
    """Serializer for address document."""

    class Meta(object):
        """Meta options."""

        document = AddressDocument
        fields = (
            'id',
            'name',
            'info',
            'city',
            'location',
        )
