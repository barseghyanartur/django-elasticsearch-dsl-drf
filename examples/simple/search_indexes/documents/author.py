from django.conf import settings

from django_elasticsearch_dsl import DocType, Index, fields

from books.models import Author

__all__ = ('AuthorDocument',)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@INDEX.doc_type
class AuthorDocument(DocType):
    """Author Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    name = fields.StringField(
        fields={
            'raw': fields.StringField(analyzer='keyword'),
            'suggest': fields.CompletionField(),
        }
    )

    salutation = fields.StringField(
        fields={
            'raw': fields.StringField(analyzer='keyword'),
            'suggest': fields.CompletionField(),
        }
    )

    email = fields.StringField(
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )

    birth_date = fields.DateField()

    biography = fields.StringField()

    phone_number = fields.StringField()

    website = fields.StringField()

    headshot = fields.StringField(attr='headshot_indexing')

    class Meta(object):
        """Meta options."""

        model = Author  # The model associate with this DocType
