import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import AuthorDocument, BookDocument, PublisherDocument

__all__ = (
    'AuthorDocumentSimpleSerializer',
    'BookDocumentSerializer',
    'BookDocumentSimpleSerializer',
    'PublisherDocumentSerializer',
    'PublisherDocumentSimpleSerializer',
)


class AuthorDocumentSimpleSerializer(DocumentSerializer):
    """Serializer for the Author document."""

    class Meta(object):
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

    # def get_id(self, obj):
    #     """Get id."""
    #     return int(obj.meta.id)

    def get_tags(self, obj):
        """Get tags."""
        return json.loads(obj.tags)


class BookDocumentSimpleSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    tags = serializers.SerializerMethodField()

    class Meta(object):
        """Meta options."""

        document = BookDocument
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

    def get_tags(self, obj):
        """Get tags."""
        if obj.tags:
            return list(obj.tags)
        else:
            return []


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
        except:
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
