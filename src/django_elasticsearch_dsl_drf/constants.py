"""
Constants module. Contains Elasticsearch constants, lookup constants,
functional constants, suggesters, etc.
"""

__title__ = 'django_elasticsearch_dsl_drf.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'ALL_GEO_SPATIAL_LOOKUP_FILTERS_AND_QUERIES',
    'ALL_LOOKUP_FILTERS_AND_QUERIES',
    'ALL_SUGGESTERS',
    'EXTENDED_NUMBER_LOOKUP_FILTERS',
    'EXTENDED_STRING_LOOKUP_FILTERS',
    'FALSE_VALUES',
    'LOOKUP_FILTER_EXISTS',
    'LOOKUP_FILTER_GEO_BOUNDING_BOX',
    'LOOKUP_FILTER_GEO_DISTANCE',
    'LOOKUP_FILTER_GEO_POLYGON',
    'LOOKUP_FILTER_PREFIX',
    'LOOKUP_FILTER_RANGE',
    'LOOKUP_FILTER_TERM',
    'LOOKUP_FILTER_TERMS',
    'LOOKUP_FILTER_WILDCARD',
    'LOOKUP_QUERY_CONTAINS',
    'LOOKUP_QUERY_ENDSWITH',
    'LOOKUP_QUERY_EXCLUDE',
    'LOOKUP_QUERY_IN',
    'LOOKUP_QUERY_ISNULL',
    'LOOKUP_QUERY_STARTSWITH',
    'NUMBER_LOOKUP_FILTERS',
    'SEARCH_QUERY_PARAM',
    'SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE',
    'SEPARATOR_LOOKUP_COMPLEX_VALUE',
    'SEPARATOR_LOOKUP_FILTER',
    'SEPARATOR_LOOKUP_VALUE',
    'STRING_LOOKUP_FILTERS',
    'SUGGESTER_COMPLETION',
    'SUGGESTER_PHRASE',
    'SUGGESTER_TERM',
    'TRUE_VALUES',
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

# Lookup filter value complex separator. To be used with geo-spatial features.
SEPARATOR_LOOKUP_COMPLEX_VALUE = ':'

SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE = ','

# Search query param
SEARCH_QUERY_PARAM = 'q'

# Geo distance ordering param
GEO_DISTANCE_ORDERING_PARAM = 'ordering'

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

# ****************************************************************************
# ******************* Native geo-spatial lookup filters/queries **************
# ****************************************************************************

# Draws a circle around the specified location and finds all documents that
# have a geo-point within that circle.
#
# The `geo_distance` filter. Accepts three values (distance|lat|lon)
# separated by `SEPARATOR_LOOKUP_VALUE`.
# https://www.elastic.co/guide/en/elasticsearch/guide/current/geo-distance.html
#
# Example:
#
# {
#     "query": {
#         "bool" : {
#             "must" : {
#                 "match_all" : {}
#             },
#             "filter" : {
#                 "geo_distance" : {
#                     "distance" : "200km",
#                     "pin.location" : {
#                         "lat" : 40,
#                         "lon" : -70
#                     }
#                 }
#             }
#         }
#     }
#     }
#
# Example: http://localhost:8000
# /api/articles/?location__geo_distance=2km|43.53455243|-12.2344243
LOOKUP_FILTER_GEO_DISTANCE = 'geo_distance'

# Geo Polygon Query
#
# A query allowing to include hits that only fall within a polygon of points.
# Example:
#
# {
#     "query": {
#         "bool" : {
#             "must" : {
#                 "match_all" : {}
#             },
#             "filter" : {
#                 "geo_polygon" : {
#                     "person.location" : {
#                         "points" : [
#                         {"lat" : 40, "lon" : -70},
#                         {"lat" : 30, "lon" : -80},
#                         {"lat" : 20, "lon" : -90}
#                         ]
#                     }
#                 }
#             }
#         }
#     }
# }
#
# Query options:
#
# - _name: Optional name field to identify the filter
# - validation_method: Set to IGNORE_MALFORMED to accept geo points with
#   invalid latitude or longitude, COERCE to try and infer correct latitude or
#   longitude, or STRICT (default is STRICT).
#
# Example: http://localhost:8000
# /api/articles/?location__geo_polygon=40,-70|30,-80|20,-90
LOOKUP_FILTER_GEO_POLYGON = 'geo_polygon'

# Geo Bounding Box Query
# A query allowing to filter hits based on a point location using a bounding
# box. Assuming the following indexed document:
#
# Example:
#
# {
#     "query": {
#         "bool" : {
#             "must" : {
#                 "match_all" : {}
#             },
#             "filter" : {
#                 "geo_bounding_box" : {
#                     "location" : {
#                         "top_left" : {
#                             "lat" : 40.73,
#                             "lon" : -74.1
#                         },
#                         "bottom_right" : {
#                             "lat" : 40.01,
#                             "lon" : -71.12
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }
#
# Query options:
#
# - _name: Optional name field to identify the filter
# - validation_method: Set to IGNORE_MALFORMED to accept geo points with
#   invalid latitude or longitude, COERCE to try and infer correct latitude or
#   longitude, or STRICT (default is STRICT).
# - type: Set to one of indexed or memory to defines whether this filter will
#   be executed in memory or indexed. See Type below for further details.
#   Default is memory.
#
# Example: http://localhost:8000
# /api/articles/?location__geo_bounding_box=40.73,-74.1|40.01,-71.12
LOOKUP_FILTER_GEO_BOUNDING_BOX = 'geo_bounding_box'

# ****************************************************************************
# ************************ Functional filters/queries ************************
# ****************************************************************************
# Lookup queries that are not native to Elasticsearch, but rather handy/easy
# to use. Inspired by Django's ORM lookups and other sources.
# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#id4

# A single value
# http://localhost:8000/api/articles/?state__endswith=lishe
LOOKUP_QUERY_CONTAINS = 'contains'

# Multiple values.
# Example: http://localhost:8000/api/articles/?tags__in=children|python
LOOKUP_QUERY_IN = 'in'

# A single value
# Example: http://localhost:8000/api/articles/?id__gt=1
# Example: http://localhost:8000/api/articles/?id__gt=1|2.0
# https://www.elastic.co/guide/en/elasticsearch/reference/1.6/
# query-dsl-range-filter.html
LOOKUP_QUERY_GT = 'gt'

# A single value
# Example: http://localhost:8000/api/articles/?id__gte=1
# Example: http://localhost:8000/api/articles/?id__gte=1|2.0
# https://www.elastic.co/guide/en/elasticsearch/reference/1.6/
# query-dsl-range-filter.html
LOOKUP_QUERY_GTE = 'gte'

# A single value
# Example: http://localhost:8000/api/articles/?id__lt=1
# Example: http://localhost:8000/api/articles/?id__lt=1|2.0
# https://www.elastic.co/guide/en/elasticsearch/reference/1.6/
# query-dsl-range-filter.html
LOOKUP_QUERY_LT = 'lt'

# A single value
# Example: http://localhost:8000/api/articles/?id__lte=1
# Example: http://localhost:8000/api/articles/?id__lte=1|2.0
# https://www.elastic.co/guide/en/elasticsearch/reference/1.6/
# query-dsl-range-filter.html
LOOKUP_QUERY_LTE = 'lte'

# A single value. Alias of `prefix`.
# Example: http://localhost:8000/api/articles/?tags__startswith=chil
LOOKUP_QUERY_STARTSWITH = 'startswith'

# A single value
# Example: http://localhost:8000/api/articles/?tags__endswith=dren
# Example: http://localhost:8000/api/articles/?state__endswith=lished
LOOKUP_QUERY_ENDSWITH = 'endswith'

# A single value
# Example: http://localhost:8000/api/articles/?tags__isnull=true
LOOKUP_QUERY_ISNULL = 'isnull'

# Multiple values.
# Example: http://localhost:8000/api/articles/?tags__exclude=children
LOOKUP_QUERY_EXCLUDE = 'exclude'

# ****************************************************************************
# *************************** Suggestions filters ****************************
# ****************************************************************************
# http://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#suggestions

# The `term` suggester
# http://127.0.0.1:8000/search/books/?title_suggest__term=Lore
SUGGESTER_TERM = 'term'

# The `phrase` suggester
# http://127.0.0.1:8000/search/books/?title_suggest__phrase=Lorem
SUGGESTER_PHRASE = 'phrase'

# The `completion` suggester
# http://127.0.0.1:8000/search/books/?title_suggest__completion=Lore
SUGGESTER_COMPLETION = 'completion'

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
    # LOOKUP_FILTER_REGEXP,
    # LOOKUP_FILTER_FUZZY,
    # LOOKUP_FILTER_TYPE,

    # Functional
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_STARTSWITH,
    LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_EXCLUDE,
)

ALL_SUGGESTERS = (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
)

ALL_GEO_SPATIAL_LOOKUP_FILTERS_AND_QUERIES = (
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
)

STRING_LOOKUP_FILTERS = [
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_STARTSWITH,
    LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_EXCLUDE,
]

EXTENDED_STRING_LOOKUP_FILTERS = STRING_LOOKUP_FILTERS + [
    LOOKUP_FILTER_EXISTS,
    LOOKUP_QUERY_ISNULL,
]

NUMBER_LOOKUP_FILTERS = [
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
]

EXTENDED_NUMBER_LOOKUP_FILTERS = NUMBER_LOOKUP_FILTERS + [
    LOOKUP_FILTER_EXISTS,
    LOOKUP_QUERY_ISNULL,
]
