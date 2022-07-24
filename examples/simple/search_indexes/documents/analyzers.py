from anysearch import OPENSEARCH, SEARCH_BACKEND
from anysearch.search_dsl import analyzer
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_7_0

__all__ = (
    'html_strip',
)

# The ``standard`` filter has been removed in Elasticsearch 7.x.
if ELASTICSEARCH_GTE_7_0 or SEARCH_BACKEND == OPENSEARCH:
    _filters = ["lowercase", "stop", "snowball"]
else:
    _filters = ["standard", "lowercase", "stop", "snowball"]

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=_filters,
    char_filter=["html_strip"]
)
