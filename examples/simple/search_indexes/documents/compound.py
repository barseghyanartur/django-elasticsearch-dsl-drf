import datetime
import os
from elasticsearch_dsl import connections
from elasticsearch_dsl import (
    analyzer,
    Boolean,
    Completion,
    Date,
    Document,
    InnerDoc,
    Keyword,
    Nested,
    Text,
    Integer,
    Float,
)
from .analyzers import html_strip
from .settings import ELASTICSEARCH_CONNECTION

try:
    from elasticsearch import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

__all__ = (
    'CompoundDocument',
)

connections.create_connection(**ELASTICSEARCH_CONNECTION)


class CompoundDocument(Document):
    title = Text(
        analyzer=html_strip,
        fields={
            'raw': Keyword(),
            'suggest': Completion(),
        }
    )
    content = Text(analyzer=html_strip)
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )
    tags = Text(
        analyzer=html_strip,
        fields={
            'raw': Keyword(multi=True),
            'suggest': Completion(multi=True),
        },
        multi=True
    )
    num_views = Integer()

    class Index:
        name = 'test_*'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'blocks': {'read_only_allow_delete': None},
        }

    # This is a hack, at the moment
    class Django:
        model = None

    def add_tag(self, name):
        self.tags.append(name)

    def save(self, ** kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        return super().save(** kwargs)
