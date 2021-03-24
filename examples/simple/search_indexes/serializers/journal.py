from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import JournalDocument

__all__ = (
    'JournalDocumentSerializer',
)


# class JournalDocumentSerializer(serializers.Serializer):
#     """Serializer for the Book document."""
#
#     isbn = serializers.CharField(read_only=True)
#
#     title = serializers.CharField(read_only=True)
#     description = serializers.CharField(read_only=True)
#     summary = serializers.CharField(read_only=True)
#
#     publication_date = serializers.DateField(read_only=True)
#
#     price = serializers.FloatField(read_only=True)
#     pages = serializers.IntegerField(read_only=True)
#     stock_count = serializers.IntegerField(read_only=True)
#     created = serializers.DateTimeField(read_only=True)
#
#     class Meta:
#         """Meta options."""
#
#         fields = (
#             'title',
#             'description',
#             'summary',
#             'publication_date',
#             'state',
#             'isbn',
#             'price',
#             'pages',
#             'stock_count',
#             'created',
#         )
#         read_only_fields = fields
#
#     def create(self, validated_data):
#         """Create.
#
#         Do nothing.
#
#         :param validated_data:
#         :return:
#         """
#
#     def update(self, instance, validated_data):
#         """Update.
#
#         Do nothing.
#
#         :param instance:
#         :param validated_data:
#         :return:
#         """


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
