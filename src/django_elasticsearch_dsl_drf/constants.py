"""
Constants module. Contains Elasticsearch constants, lookup constants,
functional constants, etc.
"""

__title__ = 'django_elasticsearch_dsl_drf.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TRUE_VALUES',
    'FALSE_VALUES',
    'SEPARATOR_LOOKUP_FILTER',
    'SEPARATOR_LOOKUP_VALUE',
    'SEARCH_QUERY_PARAM',
    'LOOKUP_FILTER_TERM',
    'LOOKUP_FILTER_TERMS',
    'LOOKUP_FILTER_RANGE',
    'LOOKUP_FILTER_EXISTS',
    'LOOKUP_FILTER_PREFIX',
    'LOOKUP_FILTER_WILDCARD',
    'LOOKUP_QUERY_IN',
    'LOOKUP_QUERY_STARTSWITH',
    'LOOKUP_QUERY_ISNULL',
    'LOOKUP_QUERY_EXCLUDE',
    'ALL_LOOKUP_FILTERS_AND_QUERIES',
)

# ****************************************************************************
# ****************************** True / False ********************************
# ****************************************************************************

# As mentioned in official documentation
# https://www.elastic.co/guide/en/elasticsearch/reference/current/boolean.html
# False values: false, "false", "off", "no", "0", "" (empty string), 0, 0.0
# True values: Anything that isn't false.
# Elasticsearch 5.1 currently accepts the above mentioned values during index
# time. Searching a boolean field using these pseudo-boolean values is
# deprecated. You should be using "true" or "false" instead.
# As of 5.3.0, usage of any value other than false, "false", true and "true"
# is deprecated.
# For the time being we'are supporting all values, but you are not recommended
# to use anything except: true, "true", false, "false".

# True values
TRUE_VALUES = (
    'true',
    '"true"',
    '1',  # To be deprecated
)

# False values
FALSE_VALUES = (
    'false',
    '"false"',
    '"off"',  # To be deprecated
    '"no"',  # To be deprecated
    '"0"',  # To be deprecated
    '""',  # To be deprecated
    '',  # To be deprecated
    '0',  # To be deprecated
    '0.0',  # To be deprecated
)

# ****************************************************************************
# ****************************** Lookup related ******************************
# ****************************************************************************

# Lookup separator
SEPARATOR_LOOKUP_FILTER = '__'

# Lookup filter value separator. To be used for `terms` and `range` filters
# lookups.
SEPARATOR_LOOKUP_VALUE = '|'

# Search query param
SEARCH_QUERY_PARAM = 'q'

# ****************************************************************************
# ************************ Native lookup filters/queries *********************
# ****************************************************************************
# Lookup filters and queries that are native to Elasticsearch
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# term-level-queries.html

# The `term` filter. Accepts a single value.
# Example: {"filter": {"term": {"tags": "children"}}}
# Example: http://localhost:8000/api/articles/?tags=children
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-term-query.html
LOOKUP_FILTER_TERM = 'term'

# The `terms` filter. Should accept multiple values, separated by
# `SEPARATOR_LOOKUP_VALUE`.
# Example: {"filter": {"terms": {"tags": ["python", "children"]}}}
# Example: http://localhost:8000/api/articles/?tags__terms=children|python
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-terms-query.html
LOOKUP_FILTER_TERMS = 'terms'

# The `range` filter. Accepts a pair of values separated by
# `SEPARATOR_LOOKUP_VALUE`.
# Example: {"query": {"range": {"age": {"gte": "16",
#                                       "lte": "67",
#                                       "boost": 2.0}}}}
# Example: http://localhost:8000/api/users/?age__range=16|67|2.0
# Example: {"query": {"range": {"age": {"gte": "16", "lte": "67"}}}}
# Example: http://localhost:8000/api/users/?age__range=16|67
# Example: {"query": {"range": {"age": {"gte": "16"}}}}
# Example: http://localhost:8000/api/users/?age__range=16
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-range-query.html
LOOKUP_FILTER_RANGE = 'range'

# Returns documents that have at least one non-null value in the original
# field.
# Example: {"query": {"exists": {"field": "tags"}}}
# Example: http://localhost:8000/api/articles/?tags__exists=true
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-exists-query.html
LOOKUP_FILTER_EXISTS = 'exists'

# The `prefix` filter. Accepts a single value.
# Example: {"filter": {"prefix": {"tags": "bio"}}}
# Example: http://localhost:8000/api/articles/?tags__prefix=bio
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-prefix-query.html
LOOKUP_FILTER_PREFIX = 'prefix'

# Supported wildcards are `*`, which matches any character sequence (including
# the empty one), and `?`, which matches any single character. Note that this
# query can be slow, as it needs to iterate over many terms. In order to
# prevent extremely slow wildcard queries, a wildcard term should not start
# with one of the wildcards `*` or `?`.
# Example: {"filter": {"wildcard": {"tags": "child*"}}}
# Example: http://localhost:8000/api/articles/?tags__wildcard=child*
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-wildcard-query.html
LOOKUP_FILTER_WILDCARD = 'wildcard'

# TODO: Implement
# The regexp query allows you to use regular expression term queries. See
# Regular expression syntax for details of the supported regular expression
# language. The "term queries" in that first sentence means that Elasticsearch
# will apply the regexp to the terms produced by the tokenizer for that field,
# and not to the original text of the field.
# Note: The performance of a regexp query heavily depends on the regular
# expression chosen. Matching everything like `.*` is very slow as well as
# using lookaround regular expressions. If possible, you should try to use a
# long prefix before your regular expression starts. Wildcard matchers
# like `.*?+` will mostly lower performance.
LOOKUP_FILTER_REGEXP = 'regexp'
# Example: {"query": {"regexp": {"tags": "ch.*en"}}}
# Example: http://localhost:8000/api/articles/?tags__regexp=ch.*en
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-regexp-query.html

# TODO: Implement
# The fuzzy query uses similarity based on Levenshtein edit distance.
LOOKUP_FILTER_FUZZY = 'fuzzy'

# TODO: Implement
# Filters documents matching the provided document / mapping type.
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-type-query.html
LOOKUP_FILTER_TYPE = 'type'

# TODO: Implement
# Filters documents that only have the provided ids. Note, this query uses the
# `_uid` field.
# https://www.elastic.co/guide/en/elasticsearch/reference/current/
# query-dsl-ids-query.html
LOOKUP_FILTER_IDS = 'ids'

# ****************************************************************************
# ************************ Functional filters/queries ************************
# ****************************************************************************
# Lookup queries that are not native to Elasticsearch, but rather handy/easy
# to use. Inspired by Django's ORM lookups and other sources.
# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#id4

# TODO: Implement
# A single value
LOOKUP_QUERY_CONTAINS = 'contains'

# Multiple values.
# Example: http://localhost:8000/api/articles/?tags__in=children|python
LOOKUP_QUERY_IN = 'in'

# TODO: Implement
# A single value
LOOKUP_QUERY_GT = 'gt'

# TODO: Implement
# A single value
LOOKUP_QUERY_GTE = 'gte'

# TODO: Implement
# A single value
LOOKUP_QUERY_LT = 'lt'

# TODO: Implement
# A single value
LOOKUP_QUERY_LTE = 'lte'

# A single value. Alias of `prefix`.
# Example: http://localhost:8000/api/articles/?tags__startswith=chil
LOOKUP_QUERY_STARTSWITH = 'startswith'

# TODO: Implement
# A single value
# Example: http://localhost:8000/api/articles/?tags__endswith=dren
LOOKUP_QUERY_ENDSWITH = 'endswith'

# A single value
# Example: http://localhost:8000/api/articles/?tags__isnull=true
LOOKUP_QUERY_ISNULL = 'isnull'

# Multiple values.
# Example: http://localhost:8000/api/articles/?tags__exclude=children
LOOKUP_QUERY_EXCLUDE = 'exclude'

# ****************************************************************************
# ******************************* Combinations *******************************
# ****************************************************************************
# Combinations of multiple constants.

# All lookup filters and queries
ALL_LOOKUP_FILTERS_AND_QUERIES = (
    # Native
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_EXISTS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_FILTER_REGEXP,
    # LOOKUP_FILTER_FUZZY,

    # Functional
    # LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_IN,
    # LOOKUP_QUERY_GT,
    # LOOKUP_QUERY_GTE,
    # LOOKUP_QUERY_LT,
    # LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_STARTSWITH,
    # LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_EXCLUDE,
)
