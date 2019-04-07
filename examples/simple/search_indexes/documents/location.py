from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from elasticsearch_dsl import analyzer

from books.models import Location

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={'read_only_allow_delete': False},
)

html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class LocationDocument(DocType):
    """
    Location document.
    """
    full = fields.StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
            "context": fields.CompletionField(
                contexts=[
                    {
                        "name": "category",
                        "type": "category",
                        "path": "category.raw",
                    },
                    {
                        "name": "occupied",
                        "type": "category",
                        "path": "occupied.raw",
                    },
                ]
            ),
            # edge_ngram_completion
            "q": StringField(
                analyzer=edge_ngram_completion
                ),
        }
    )
    partial = fields.StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
            "context": fields.CompletionField(
                contexts=[
                    {
                        "name": "category",
                        "type": "category",
                        "path": "category.raw",
                    },
                    {
                        "name": "occupied",
                        "type": "category",
                        "path": "occupied.raw",
                    },
                ]
            ),
            # edge_ngram_completion
            "q": StringField(
                analyzer=edge_ngram_completion
                ),
        }
    )
    postcode = fields.StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
            "context": fields.CompletionField(
                contexts=[
                    {
                        "name": "category",
                        "type": "category",
                        "path": "category.raw",
                    },
                    {
                        "name": "occupied",
                        "type": "category",
                        "path": "occupied.raw",
                    },
                ]
            ),
        }
    )
    number = fields.StringField(
        attr="address_no",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    address = fields.StringField(
        attr="address_street",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    town = fields.StringField(
        attr="address_town",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    authority = fields.StringField(
        attr="authority_name",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    # URL fields /geocode/slug
    geocode = fields.StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    slug = fields.StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    # Filter fields
    category = fields.StringField(
        attr="group",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    occupied = fields.StringField(
        attr="occupation_status_text",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )
    size = fields.FloatField(attr="floor_area")
    staff = fields.FloatField(attr="employee_count")
    rent = fields.FloatField(attr="rental_valuation")
    revenue = fields.FloatField(attr="revenue")
    coordinates = fields.GeoPointField(attr="location_field_indexing")

    class Meta(object):
        """Meta options."""

        model = Location  # The model associate with this DocType
        parallel_indexing = True
        queryset_pagination = 1000  # This will split the queryset
                                    # into parts while indexing
