from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import TagDocument, NoKeywordTagDocument


__all__ = ('TagDocumentSerializer',
           'NoKeywordTagDocumentSerializer')


class TagDocumentSerializer(DocumentSerializer):
    """Serializer for a Tag document."""

    class Meta:
        """Meta options."""

        document = TagDocument
        fields = (
            'id',
            'title',
        )


class NoKeywordTagDocumentSerializer(DocumentSerializer):
    """Serializer for a Tag document."""

    class Meta:
        """Meta options."""

        document = NoKeywordTagDocument
        fields = (
            'id',
            'title',
        )
