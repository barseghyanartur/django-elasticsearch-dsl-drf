from django.conf import settings

from anysearch.django_search_dsl import Document, fields
from anysearch.django_search_dsl import registries
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

from books.models import City

from .analyzers import html_strip


__all__ = ('CityDocument',)

@registries.registry.register_document
class CityDocument(Document):
    """City Elasticsearch document.

    This document has been created purely for testing out complex fields.
    """

    # In different parts of the code different fields are used. There are
    # a couple of use cases: (1) more-like-this functionality, where `title`,
    # `description` and `summary` fields are used, (2) search and filtering
    # functionality where all of the fields are used.

    # ID
    id = fields.IntegerField(attr='id')

    # ********************************************************************
    # ********************** Main data fields for search *****************
    # ********************************************************************

    name = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    info = StringField(analyzer=html_strip)

    # ********************************************************************
    # ************** Nested fields for search and filtering **************
    # ********************************************************************

    # City object
    country = fields.NestedField(
        properties={
            'name': StringField(
                analyzer=html_strip,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            ),
            'info': StringField(analyzer=html_strip),
            'location': fields.GeoPointField(attr='location_field_indexing'),
        }
    )

    location = fields.GeoPointField(attr='location_field_indexing')

    # ********************************************************************
    # ********** Other complex fields for search and filtering ***********
    # ********************************************************************

    boolean_list = fields.ListField(
        StringField(attr='boolean_list_indexing')
    )
    # boolean_dict_indexing = fields.ObjectField(
    #     properties={
    #         'true': fields.BooleanField(),
    #         'false': fields.BooleanField(),
    #     }
    # )
    datetime_list = fields.ListField(
        StringField(attr='datetime_list_indexing')
    )
    # datetime_dict_indexing
    float_list = fields.ListField(
        StringField(attr='float_list_indexing')
    )
    # float_dict_indexing
    integer_list = fields.ListField(
        StringField(attr='integer_list_indexing')
    )
    # integer_dict_indexing

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        model = City  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing
