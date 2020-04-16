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
from .settings import BLOG_POST_DOCUMENT_NAME, ELASTICSEARCH_CONNECTION

try:
    from elasticsearch import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

__all__ = (
    'Comment',
    'PostDocument',
)

connections.create_connection(**ELASTICSEARCH_CONNECTION)


class Comment(InnerDoc):
    author = Text(fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    created_at = Date()

    def age(self):
        return datetime.datetime.now() - self.created_at


class PostDocument(Document):
    title = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )
    # title_suggest = Completion()
    content = Text()
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )
    comments = Nested(Comment)
    tags = Text(
        analyzer=html_strip,
        fields={'raw': Keyword(multi=True)},
        multi=True
    )
    num_views = Integer()

    class Index:
        name = BLOG_POST_DOCUMENT_NAME
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'blocks': {'read_only_allow_delete': None},
        }

    # This is a hack, at the moment
    class Django:
        model = None

    def add_comment(self, author, content):
        self.comments.append(
            Comment(
                author=author,
                content=content,
                created_at=datetime.datetime.now()
            )
        )

    def add_tag(self, name):
        self.tags.append(name)

    def save(self, ** kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        return super().save(** kwargs)


try:
    # Create the mappings in Elasticsearch
    PostDocument.init()
except Exception as err:
    logger.error(err)
