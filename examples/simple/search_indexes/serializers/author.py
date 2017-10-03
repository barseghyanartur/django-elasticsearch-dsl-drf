from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import AuthorDocument

__all__ = ('AuthorDocumentSimpleSerializer',)


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
