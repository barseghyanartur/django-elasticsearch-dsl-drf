from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    AddressDocumentViewSet,
    AuthorDocumentViewSet,
    BookCompoundFuzzySearchBackendDocumentViewSet,
    BookCompoundSearchBackendDocumentViewSet,
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    BookCustomDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookFrontendDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookIgnoreIndexErrorsDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
    BookMoreLikeThisNoOptionsDocumentViewSet,
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookPermissionsDocumentViewSet,
    BookNoPermissionsDocumentViewSet,
    BookNoRecordsDocumentViewSet,
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    BookSourceSearchBackendDocumentViewSet,
    JournalDocumentViewSet,
    CityCompoundSearchBackendDocumentViewSet,
    CityDocumentViewSet,
    FrontAddressDocumentViewSet,
    LocationDocumentViewSet,
    PublisherDocumentViewSet,
    QueryFriendlyPaginationBookDocumentViewSet,
    TagDocumentViewSet,
)

__all__ = ('urlpatterns',)

router = DefaultRouter()

# **********************************************************
# *********************** Addresses ************************
# **********************************************************
router.register(
    r'addresses',
    AddressDocumentViewSet,
    basename='addressdocument'
)

router.register(
    r'addresses-frontend',
    FrontAddressDocumentViewSet,
    basename='addressdocument_frontend'
)

# **********************************************************
# ************************* Authors ************************
# **********************************************************
router.register(
    r'authors',
    AuthorDocumentViewSet,
    basename='authordocument'
)

# **********************************************************
# ************************* Authors ************************
# **********************************************************
router.register(
    r'journals',
    JournalDocumentViewSet,
    basename='journaldocument'
)

# **********************************************************
# ************************** Books *************************
# **********************************************************
router.register(
    r'books',
    BookDocumentViewSet,
    basename='bookdocument'
)

router.register(
    r'books-query-friendly-pagination',
    QueryFriendlyPaginationBookDocumentViewSet,
    basename='bookdocument_query_friendly_pagination'
)

router.register(
    r'books-ordered-by-score',
    BookOrderingByScoreDocumentViewSet,
    basename='bookdocument_ordered_by_score'
)

router.register(
    r'books-functional-suggester',
    BookFunctionalSuggesterDocumentViewSet,
    basename='bookdocument_functional_suggester'
)

router.register(
    r'books-frontend',
    BookFrontendDocumentViewSet,
    basename='bookdocument_frontend'
)

router.register(
    r'books-permissions',
    BookPermissionsDocumentViewSet,
    basename='bookdocument_permissions'
)

router.register(
    r'books-no-permissions',
    BookNoPermissionsDocumentViewSet,
    basename='bookdocument_no_permissions'
)

router.register(
    r'books-no-records',
    BookNoRecordsDocumentViewSet,
    basename='bookdocument_no_records'
)

router.register(
    r'books-custom',
    BookCustomDocumentViewSet,
    basename='bookdocument_custom'
)

router.register(
    r'books-ignore-index-errors',
    BookIgnoreIndexErrorsDocumentViewSet,
    basename='bookdocument_ignore_index_errors'
)

router.register(
    r'books-more-like-this',
    BookMoreLikeThisDocumentViewSet,
    basename='bookdocument_more_like_this'
)

router.register(
    r'books-more-like-this-no-options',
    BookMoreLikeThisNoOptionsDocumentViewSet,
    basename='bookdocument_more_like_this_no_options'
)

router.register(
    r'books-default-filter-lookup',
    BookDefaultFilterLookupDocumentViewSet,
    basename='bookdocument_default_filter_lookup'
)

router.register(
    r'books-compound-search-backend',
    BookCompoundSearchBackendDocumentViewSet,
    basename='bookdocument_compound_search_backend'
)

router.register(
    r'books-compound-fuzzy-search-backend',
    BookCompoundFuzzySearchBackendDocumentViewSet,
    basename='bookdocument_compound_fuzzy_search_backend'
)

router.register(
    r'books-compound-search-boost-backend',
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    basename='bookdocument_compound_search_boost_backend'
)

router.register(
    r'books-compound-search-backend-ordered-by-score',
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    basename='bookdocument_compound_search_backend_ordered_by_score'
)

router.register(
    r'books-source',
    BookSourceSearchBackendDocumentViewSet,
    basename='bookdocument_source'
)

router.register(
    r'books-multi-match-search-backend',
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    basename='bookdocument_multi_match_search_backend'
)

router.register(
    r'books-multi-match-phrase-prefix-search-backend',
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    basename='bookdocument_multi_match_phrase_prefix_search_backend'
)

router.register(
    r'books-simple-query-string-search-backend',
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    basename='bookdocument_simple_query_string_search_backend'
)

router.register(
    r'books-simple-query-string-boost-search-backend',
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
    basename='bookdocument_simple_query_string_boost_search_backend'
)

# **********************************************************
# ************************* Cities *************************
# **********************************************************

router.register(
    r'cities',
    CityDocumentViewSet,
    basename='citydocument'
)

router.register(
    r'cities-compound-search-backend',
    CityCompoundSearchBackendDocumentViewSet,
    basename='citydocument_compound_search_backend'
)

# **********************************************************
# *********************** Locations ************************
# **********************************************************

router.register(
    r'locations',
    LocationDocumentViewSet,
    basename='locationdocument'
)

# **********************************************************
# *********************** Publishers ***********************
# **********************************************************

router.register(
    r'publishers',
    PublisherDocumentViewSet,
    basename='publisherdocument'
)

# *********************************************************
# ************************* Tags **************************
# *********************************************************

router.register(
    r'tags',
    TagDocumentViewSet,
    basename='tagdocument'
)

# **********************************************************
# ********************** URL patterns **********************
# **********************************************************

urlpatterns = [
    url(r'^', include(router.urls)),
]
