from django_elasticsearch_dsl.registries import registry

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis

__title__ = 'django_elasticsearch_dsl_drf.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'get_document_for_model',
    'get_index_and_mapping_for_model',
    'more_like_this',
)


def get_document_for_model(model):
    """Get document for model given.

    :param model: Model to get document index for.
    :type model: Subclass of `django.db.models.Model`.
    :return: Document index for the given model.
    :rtype: Subclass of `django_elasticsearch_dsl.DocType`.
    """
    documents = registry.get_documents()
    for document in documents:
        if model == document._doc_type.model:
            return document


def get_index_and_mapping_for_model(model):
    """Get index and mapping for model.

    :param model: Django model for which to get index and mapping for.
    :type model: Subclass of `django.db.models.Model`.
    :return: Index and mapping values.
    :rtype: tuple.
    """
    document = get_document_for_model(model)
    if document is not None:
        return (
            document._doc_type.index,
            document._doc_type.mapping.properties.name
        )


def more_like_this(obj, min_term_freq=1, max_query_terms=12):
    """More like this.

    :param obj: Django model instance for which similar objects shall be found.
    :param min_term_freq:
    :param max_query_terms:
    :type obj: Instance of `django.db.models.Model` (sub-classed) model.
    :type min_term_freq: int
    :type max_query_terms: int
    :return: List of objects.
    :rtype: elasticsearch_dsl.search.Search
    """
    _index, _mapping = get_index_and_mapping_for_model(obj._meta.model)
    if _index is None:
        return None

    _client = connections.get_connection()
    _search = Search(using=_client, index=_index)

    return _search.query(
        MoreLikeThis(
            fields=['title', 'content', 'summary'],
            like={
                '_id': "{}".format(obj.pk),
                '_index': "{}".format(_index),
                '_type': "{}".format(_mapping)
            },
            min_term_freq=min_term_freq,
            max_query_terms=max_query_terms,
        )
    )
