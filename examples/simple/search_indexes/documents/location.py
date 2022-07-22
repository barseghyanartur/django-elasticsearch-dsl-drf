from django.conf import settings
from anysearch.django_search_dsl import Document, fields, registry
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0

from books.models import Location

from .analyzers import html_strip


@registry.register_document
class LocationDocument(Document):
    """
    Location document.
    """
    # Full fields
    __full_fields = {
            "raw": KeywordField(),
            # edge_ngram_completion
            "q": StringField(
                analyzer=edge_ngram_completion
            ),
        }

    if ELASTICSEARCH_GTE_5_0:
        __full_fields.update(
            {
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

    full = StringField(
        analyzer=html_strip,
        fields=__full_fields
    )

    # Partial fields
    __partial_fields = {
        "raw": KeywordField(),
        # edge_ngram_completion
        "q": StringField(
            analyzer=edge_ngram_completion
            ),
    }
    if ELASTICSEARCH_GTE_5_0:
        __partial_fields.update(
            {
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
    partial = StringField(
        analyzer=html_strip,
        fields=__partial_fields
    )

    # Postcode
    __postcode_fields = {
        "raw": KeywordField(),
    }
    if ELASTICSEARCH_GTE_5_0:
        __postcode_fields.update(
            {
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
    postcode = StringField(
        analyzer=html_strip,
        fields=__postcode_fields
    )

    # Number
    number = StringField(
        attr="address_no",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # Address
    address = StringField(
        attr="address_street",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # Town
    town = StringField(
        attr="address_town",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # Authority
    authority = StringField(
        attr="authority_name",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # URL fields /geocode/slug
    geocode = StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # Slug
    slug = StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # ********************* Filter fields **********************
    # Category
    category = StringField(
        attr="group",
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # Occupied
    occupied = StringField(
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

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        model = Location  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        queryset_pagination = 50  # This will split the queryset
                                  # into parts while indexing
