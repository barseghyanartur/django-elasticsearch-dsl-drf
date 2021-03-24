from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import TagDocument


__all__ = ('TagDocumentSerializer',)


class TagDocumentSerializer(DocumentSerializer):
    """Serializer for a Tag document."""

    class Meta:
        """Meta options."""

        document = TagDocument
        fields = (
            'id',
            'title',
        )
