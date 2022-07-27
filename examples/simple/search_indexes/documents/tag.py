from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from books.models import Tag


__all__ = ('TagDocument',)


@registry.register_document
class TagDocument(Document):
    """Elasticsearch document for a Tag."""

    # Set unique title as the document id.
    id = fields.KeywordField(attr='title')
    title = fields.KeywordField()

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        """Django Elasticsearch DSL ORM Meta."""

        model = Tag

    class Meta:
        """Meta options."""

        parellel_indexing = True
