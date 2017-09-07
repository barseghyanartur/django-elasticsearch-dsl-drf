"""
Transitional compatibility module. Contains various field wrappers and
helpers for painless (testing of) Elastic 2.x to Elastic 5.x transition. This
module is not supposed to solve all transition issues for you. Better move to
Elastic 5.x as soon as possible.
"""
from django_elasticsearch_dsl import fields

from elasticsearch import Elasticsearch

__title__ = 'django_elasticsearch_dsl_drf.compat'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'get_elasticsearch_version',
    'KeywordField',
    'StringField',
)


def get_elasticsearch_version():
    """Get Elasticsearch version.

    :return:
    :rtype: list
    """
    es = Elasticsearch()
    version = es.info()['version']['number']
    return [int(__v) for __v in version.split('.', 2)]


def keyword_field(**kwargs):
    """Keyword field.

    :param kwargs:
    :return:
    """
    major = get_elasticsearch_version()[0]
    if major > 2:
        return fields.KeywordField(**kwargs)
    else:
        if 'analyzer' not in kwargs:
            kwargs['analyzer'] = 'keyword'
        return fields.StringField(**kwargs)

KeywordField = keyword_field


def string_field(**kwargs):
    """String field.

    :param kwargs:
    :return:
    """
    major = get_elasticsearch_version()[0]
    if major > 2:
        if 'fielddata' not in kwargs:
            kwargs['fielddata'] = True
        return fields.StringField(**kwargs)
    else:
        return fields.StringField(**kwargs)

StringField = string_field
