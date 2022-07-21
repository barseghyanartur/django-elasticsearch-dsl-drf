from django.conf import settings

from anysearch.django_search_dsl import Document, fields
from anysearch.django_search_dsl import registries
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion

from books.models import Author

__all__ = ('AuthorDocument',)


@registries.registry.register_document
class AuthorDocument(Document):
    """Author Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    name = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    salutation = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    email = StringField(
        fields={
            'raw': KeywordField(),
        }
    )

    birth_date = fields.DateField()

    biography = StringField()

    phone_number = StringField()

    website = StringField()

    headshot = StringField(attr='headshot_indexing')

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        model = Author  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        # queryset_pagination = 50  # This stands for `chunk_size`
