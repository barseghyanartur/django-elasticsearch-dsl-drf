from django.conf import settings

from django_elasticsearch_dsl import DocType, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

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

    name = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    salutation = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    email = StringField(
        fields={
            'raw': KeywordField(),
        }
    )

    birth_date = fields.DateField()

    biography = StringField()

    phone_number = StringField()

    website = StringField()

    headshot = StringField(attr='headshot_indexing')

    class Meta(object):
        """Meta options."""

        model = Author  # The model associate with this DocType
