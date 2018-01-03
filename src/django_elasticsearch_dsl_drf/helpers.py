"""
Helpers.
"""
from collections import OrderedDict

from django_elasticsearch_dsl.registries import registry

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis

from six import PY3


__title__ = 'django_elasticsearch_dsl_drf.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'get_document_for_model',
    'get_index_and_mapping_for_model',
    'more_like_this',
    'sort_by_list',
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


def sort_by_list(unsorted_dict, sorted_keys):
    """Sort an OrderedDict by list of sorted keys.

    :param unsorted_dict: Source dictionary.
    :param sorted_keys: Keys to sort on.
    :type unsorted_dict: collections.OrderedDict
    :type sorted_keys: list
    :return: Sorted dictionary.
    :rtype: collections.OrderedDict
    """
    __unsorted_dict_keys = [__key for __key in unsorted_dict.keys()]
    __sorted_keys = (
        tuple(sorted_keys) + tuple(
            set(__unsorted_dict_keys) - set(sorted_keys)
        )
    )
    if PY3:
        for key in __sorted_keys:
            if key in unsorted_dict:
                unsorted_dict.move_to_end(key)

        return unsorted_dict
    else:
        sorted_dict = OrderedDict(
            (key, unsorted_dict[key]) for key in __sorted_keys
        )
        return sorted_dict


def more_like_this(obj,
                   fields,
                   max_query_terms=25,
                   min_term_freq=2,
                   min_doc_freq=5,
                   max_doc_freq=0,
                   query=None):
    """More like this.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/
    query-dsl-mlt-query.html

    :param obj: Django model instance for which similar objects shall be found.
    :param fields: Fields to search in.
    :param max_query_terms:
    :param min_term_freq:
    :param min_doc_freq:
    :param max_doc_freq:
    :param query: Q query
    :type obj: Instance of `django.db.models.Model` (sub-classed) model.
    :type fields: list
    :type max_query_terms: int
    :type min_term_freq: int
    :type min_doc_freq: int
    :type max_doc_freq: int
    :type query: elasticsearch_dsl.query.Q
    :return: List of objects.
    :rtype: elasticsearch_dsl.search.Search

    Example:

        >>> from django_elasticsearch_dsl_drf.helpers import more_like_this
        >>> from books.models import Book
        >>> book = Book.objects.first()
        >>> similar_books = more_like_this(
        >>>     book,
        >>>     ['title', 'description', 'summary']
        >>> )
    """
    _index, _mapping = get_index_and_mapping_for_model(obj._meta.model)
    if _index is None:
        return None

    _client = connections.get_connection()
    _search = Search(using=_client, index=_index)

    if query is not None:
        _search = _search.query(query)

    kwargs = {}

    if max_query_terms is not None:
        kwargs['max_query_terms'] = max_query_terms

    if min_term_freq is not None:
        kwargs['min_term_freq'] = min_term_freq

    if min_doc_freq is not None:
        kwargs['min_doc_freq'] = min_doc_freq

    if max_doc_freq is not None:
        kwargs['max_doc_freq'] = max_doc_freq

    return _search.query(
        MoreLikeThis(
            fields=fields,
            like={
                '_id': "{}".format(obj.pk),
                '_index': "{}".format(_index),
                '_type': "{}".format(_mapping)
            },
            **kwargs
        )
    )
