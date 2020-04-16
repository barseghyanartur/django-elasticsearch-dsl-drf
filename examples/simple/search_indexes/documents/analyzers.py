from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_7_0

__all__ = (
    'html_strip',
    'html_strip_preserve_case',
)

# The ``standard`` filter has been removed in Elasticsearch 7.x.
if ELASTICSEARCH_GTE_7_0:
    _filters = ["lowercase", "stop", "snowball"]
    _pc_filters = ["stop", "snowball"]
else:
    _filters = ["standard", "lowercase", "stop", "snowball"]
    _pc_filters = ["standard", "stop", "snowball"]

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=_filters,
    char_filter=["html_strip"]
)


html_strip_preserve_case = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=_pc_filters,
    char_filter=["html_strip"]
)
