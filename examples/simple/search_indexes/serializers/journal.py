from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import JournalDocument

__all__ = (
    'JournalDocumentSerializer',
)


class JournalDocumentSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    score = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""

        document = JournalDocument
        fields = (
            'title',
            'description',
            'summary',
            'publication_date',
            'isbn',
            'price',
            'pages',
            'stock_count',
            'created',
        )

    def get_score(self, obj):
        if hasattr(obj.meta, 'score'):
            return obj.meta.score
        return None
