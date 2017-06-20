from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer

from books.models import Book

from ..constants import BOOK_INDEX_NAME

__all__ = ('BookDocument',)

# Name of the ElasticSearch index
BOOK_INDEX = Index(BOOK_INDEX_NAME)
# See ElasticSearch Indices API reference for available settings
BOOK_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@BOOK_INDEX.doc_type
class BookDocument(DocType):
    """Book ElasticSearch document."""

    # In different parts of the code different fields are used. There are
    # a couple of use cases: (1) more-like-this functionality, where `title`,
    # `description` and `summary` fields are used, (2) search and filtering
    # functionality where all of the fields are used.

    # ID
    id = fields.IntegerField(attr='id')

    # ********************************************************************
    # *********************** Main data fields for search ****************
    # ********************************************************************

    title = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    description = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    summary = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    # ********************************************************************
    # ********** Additional fields for search and filtering **************
    # ********************************************************************

    # Publisher
    publisher = fields.StringField(
        attr='publisher_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    # Publication date
    publication_date = fields.DateField()

    # State
    state = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    # ISBN
    isbn = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword'
            )
        }
    )

    # Price
    price = fields.FloatField()

    # Pages
    pages = fields.IntegerField()

    # Stock count
    stock_count = fields.IntegerField()

    # Tags
    tags = fields.StringField(
        attr='tags_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(
                analyzer='keyword',
                multi=True
            )
        },
        multi=True
    )

    class Meta(object):
        """Meta options."""

        model = Book  # The model associate with this DocType
