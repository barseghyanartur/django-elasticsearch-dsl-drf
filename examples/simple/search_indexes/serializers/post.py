from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from django_elasticsearch_dsl_drf import fields

from ..documents import PostDocument

__all__ = ('PostDocumentSerializer',)


class PostDocumentSerializer(DocumentSerializer):
    """Serializer for post document."""

    id = fields.IntegerField(read_only=True)
    title = fields.CharField(read_only=True)
    content = fields.CharField(read_only=True)
    created_at = fields.DateField(read_only=True)
    published = fields.BooleanField(read_only=True)
    category = fields.CharField(read_only=True)
    comments = fields.ListField(read_only=True)
    tags = fields.ListField(read_only=True)
    num_views = fields.IntegerField()

    class Meta(object):
        """Meta options."""

        document = PostDocument
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'published',
            'category',
            # 'comments',
            # 'tags',
            'num_views',
        )
