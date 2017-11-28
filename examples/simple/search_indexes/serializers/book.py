from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import BookDocument

__all__ = (
    'BookDocumentSerializer',
    'BookDocumentSimpleSerializer',
)


class BookDocumentSerializer(serializers.Serializer):
    """Serializer for the Book document."""

    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    summary = serializers.CharField(read_only=True)

    publisher = serializers.CharField(read_only=True)
    publication_date = serializers.DateField(read_only=True)
    state = serializers.CharField(read_only=True)
    isbn = serializers.CharField(read_only=True)
    price = serializers.FloatField(read_only=True)
    pages = serializers.IntegerField(read_only=True)
    stock_count = serializers.IntegerField(read_only=True)
    tags = serializers.SerializerMethodField()

    # Used in testing of `isnull` functional filter.
    null_field = serializers.CharField(read_only=True,
                                       required=False,
                                       allow_blank=True)

    class Meta(object):
        """Meta options."""

        fields = (
            'id',
            'title',
            'description',
            'summary',
            'publisher',
            'publication_date',
            'state',
            'isbn',
            'price',
            'pages',
            'stock_count',
            'tags',
            'null_field',  # Used in testing of `isnull` functional filter.
        )
        read_only_fields = fields

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

    def get_tags(self, obj):
        """Get tags."""
        if obj.tags:
            return list(obj.tags)
        else:
            return []


class BookDocumentSimpleSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    # tags = serializers.SerializerMethodField()
    # authors = serializers.SerializerMethodField()
    highlight = serializers.SerializerMethodField()

    class Meta(object):
        """Meta options."""

        document = BookDocument
        fields = (
            'id',
            'title',
            'description',
            'summary',
            'authors',
            'publisher',
            'publication_date',
            'state',
            'isbn',
            'price',
            'pages',
            'stock_count',
            'tags',
            'highlight',  # Used in highlight tests
            'null_field',  # Used in testing of `isnull` functional filter.
        )

    def get_highlight(self, obj):
        if hasattr(obj.meta, 'highlight'):
            return obj.meta.highlight.__dict__['_d_']
        return {}
