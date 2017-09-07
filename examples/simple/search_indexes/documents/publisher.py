from django.conf import settings

from django_elasticsearch_dsl import DocType, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

from books.models import Publisher

__all__ = ('PublisherDocument',)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@INDEX.doc_type
class PublisherDocument(DocType):
    """Publisher Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    name = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
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
        }
    )

    state_province = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    country = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    website = StringField()

    class Meta(object):
        """Meta options."""

        model = Publisher  # The model associate with this DocType
