"""
Analyzers.
"""
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.analysis import token_filter

__title__ = 'django_elasticsearch_dsl_drf.analyzers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'edge_ngram_completion_filter',
    'edge_ngram_completion',
)

edge_ngram_completion_filter = token_filter(
    'edge_ngram_completion_filter',
    type="edge_ngram",
    min_gram=1,
    max_gram=20
)


edge_ngram_completion = analyzer(
    "edge_ngram_completion",
    tokenizer="standard",
    filter=["lowercase", edge_ngram_completion_filter]
)
