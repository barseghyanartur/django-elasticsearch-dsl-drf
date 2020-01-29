import datetime
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
)
from .settings import SITE_USER_DOCUMENT_NAME, ELASTICSEARCH_CONNECTION

try:
    from elasticsearch import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

__all__ = (
    'SiteUser',
)

connections.create_connection(**ELASTICSEARCH_CONNECTION)


html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


class SiteUser(Document):
    first_name = Text(fields={'raw': Keyword()})
    last_name = Text(fields={'raw': Keyword()})
    email = Text(fields={'raw': Keyword()})
    created_at = Date()
    is_active = Boolean()

    class Index:
        name = SITE_USER_DOCUMENT_NAME
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'blocks': {'read_only_allow_delete': None},
        }

    def save(self, ** kwargs):
        self.created_at = datetime.datetime.now()
        return super().save(** kwargs)


try:
    # Create the mappings in Elasticsearch
    SiteUser.init()
except Exception as err:
    logger.error(err)
