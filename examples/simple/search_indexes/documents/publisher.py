from django_elasticsearch_dsl import DocType, Index, fields

from books.models import Publisher

from ..constants import PUBLISHER_INDEX_NAME

# Name of the ElasticSearch index
PUBLISHER_INDEX = Index(PUBLISHER_INDEX_NAME)
# See ElasticSearch Indices API reference for available settings
PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@PUBLISHER_INDEX.doc_type
class PublisherDocument(DocType):
    """Publisher ElasticSearch document."""

    id = fields.IntegerField(attr='id')

    name = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )
    address = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )
    city = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )
    state_province = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )
    country = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )
    website = fields.StringField(
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    class Meta(object):
        """Meta options."""

        model = Publisher  # The model associate with this DocType
