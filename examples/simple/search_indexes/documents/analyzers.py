from elasticsearch_dsl import analyzer
from elasticsearch_dsl.analysis import token_filter

__all__ = (
    'autocomplete',
    'autocomplete_filter',
    'html_strip',
)

# TODO: Perhaps move to the main package
autocomplete_filter = token_filter(
    'autocomplete_filter',
    type="edge_ngram",
    min_gram=1,
    max_gram=20
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

# TODO: Perhaps move to the main package
autocomplete = analyzer(
    "autocomplete",
    tokenizer="standard",
    filter=["lowercase", autocomplete_filter]
)
