from django.conf import settings

from anysearch.django_search_dsl import Document, fields
from anysearch.django_search_dsl import registries
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion

from books.models import Publisher

__all__ = ('PublisherDocument',)


@registries.registry.register_document
class PublisherDocument(Document):
    """Publisher Elasticsearch document."""

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

    info = StringField()

    address = StringField(
        fields={
            'raw': KeywordField()
        }
    )

    city = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    state_province = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    country = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    website = StringField()

    # Location
    location = fields.GeoPointField(attr='location_field_indexing')

    # Geo-shape fields
    location_point = fields.GeoShapeField(strategy='recursive',
                                          attr='location_point_indexing')
    location_circle = fields.GeoShapeField(strategy='recursive',
                                           attr='location_circle_indexing')

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        model = Publisher  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing
