from django.conf import settings

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0

from books.models import Book

from .analyzers import html_strip


__all__ = ('BookDocument',)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={'read_only_allow_delete': None},
    # read_only_allow_delete=False
)


@INDEX.doc_type
class BookDocument(Document):
    """Book Elasticsearch document."""

    # In different parts of the code different fields are used. There are
    # a couple of use cases: (1) more-like-this functionality, where `title`,
    # `description` and `summary` fields are used, (2) search and filtering
    # functionality where all of the fields are used.

    # ID
    id = fields.IntegerField(attr='id')

    # ********************************************************************
    # *********************** Main data fields for search ****************
    # ********************************************************************
    __title_fields = {
        'raw': KeywordField(),
        'suggest': fields.CompletionField(),
        'edge_ngram_completion': StringField(
            analyzer=edge_ngram_completion
        ),
        'mlt': StringField(analyzer='english'),
    }

    if ELASTICSEARCH_GTE_5_0:
        __title_fields.update(
            {
                'suggest_context': fields.CompletionField(
                    contexts=[
                        {
                            "name": "tag",
                            "type": "category",
                            "path": "tags.raw",
                        },
                        {
                            "name": "state",
                            "type": "category",
                            "path": "state.raw",
                        },
                        {
                            "name": "publisher",
                            "type": "category",
                            "path": "publisher.raw",
                        },
                    ]
                ),
            }
        )

    title = StringField(
        analyzer=html_strip,
        fields=__title_fields
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

    authors = fields.ListField(
        StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
            }
        )
    )

    # Publisher
    publisher = StringField(
        attr='publisher_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    # Publication date
    publication_date = fields.DateField()

    # State
    state = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )

    # ISBN
    isbn = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )

    # Price
    price = fields.FloatField()

    # Pages
    pages = fields.IntegerField()

    # Stock count
    stock_count = fields.IntegerField()

    # Tags
    tags = StringField(
        attr='tags_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    # Date created
    created = fields.DateField()

    null_field = StringField(attr='null_field_indexing')

    class Django(object):
        model = Book  # The model associate with this Document

    class Meta(object):
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing

    def prepare_summary(self, instance):
        """Prepare summary."""
        return instance.summary[:32766] if instance.summary else None

    def prepare_authors(self, instance):
        """Prepare authors."""
        return [author.name for author in instance.authors.all()]

