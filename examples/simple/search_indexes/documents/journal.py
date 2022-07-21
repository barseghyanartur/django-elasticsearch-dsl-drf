from django.conf import settings

from anysearch.django_search_dsl import Document, fields
from anysearch.django_search_dsl import registries
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0

from books.models import Journal

from .analyzers import html_strip


__all__ = ('JournalDocument',)


@registries.registry.register_document
class JournalDocument(Document):
    """Journal Elasticsearch document."""

    # In different parts of the code different fields are used. There are
    # a couple of use cases: (1) more-like-this functionality, where `title`,
    # `description` and `summary` fields are used, (2) search and filtering
    # functionality where all of the fields are used.

    # ISBN/ID
    isbn = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )

    # ********************************************************************
    # *********************** Main data fields for search ****************
    # ********************************************************************

    title = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
            'mlt': StringField(analyzer='english'),
        }
    )

    description = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'mlt': StringField(analyzer='english'),
        }
    )

    summary = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'mlt': StringField(analyzer='english'),
        }
    )

    # ********************************************************************
    # ********** Additional fields for search and filtering **************
    # ********************************************************************

    # Publication date
    publication_date = fields.DateField()

    # Price
    price = fields.FloatField()

    # Pages
    pages = fields.IntegerField()

    # Stock count
    stock_count = fields.IntegerField()

    # Date created
    created = fields.DateField(attr='created_indexing')

    # See Elasticsearch Indices API reference for available settings
    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks": {"read_only_allow_delete": False},
        }

    class Django(object):
        model = Journal  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing

    def prepare_summary(self, instance):
        """Prepare summary."""
        return instance.summary[:32766] if instance.summary else None
