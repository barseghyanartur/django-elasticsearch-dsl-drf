from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    AddressDocumentViewSet,
    AuthorDocumentViewSet,
    BookCompoundSearchBackendDocumentViewSet,
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookFrontendDocumentViewSet,
    BookCustomDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookIgnoreIndexErrorsDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
    BookMoreLikeThisNoOptionsDocumentViewSet,
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    BookPermissionsDocumentViewSet,
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    BookSourceSearchBackendDocumentViewSet,
    CityCompoundSearchBackendDocumentViewSet,
    CityDocumentViewSet,
    LocationDocumentViewSet,
    PublisherDocumentViewSet,
    FrontAddressDocumentViewSet,
)

__all__ = ('urlpatterns',)

router = DefaultRouter()

# **********************************************************
# *********************** Addresses ************************
# **********************************************************
router.register(
    r'addresses',
    AddressDocumentViewSet,
    base_name='addressdocument'
)

router.register(
    r'addresses-frontend',
    FrontAddressDocumentViewSet,
    base_name='addressdocument_frontend'
)

# **********************************************************
# ************************* Authors ************************
# **********************************************************
router.register(
    r'authors',
    AuthorDocumentViewSet,
    base_name='authordocument'
)

# **********************************************************
# ************************** Books *************************
# **********************************************************
router.register(
    r'books',
    BookDocumentViewSet,
    base_name='bookdocument'
)

router.register(
    r'books-ordered-by-score',
    BookOrderingByScoreDocumentViewSet,
    base_name='bookdocument_ordered_by_score'
)

router.register(
    r'books-functional-suggester',
    BookFunctionalSuggesterDocumentViewSet,
    base_name='bookdocument_functional_suggester'
)

router.register(
    r'books-frontend',
    BookFrontendDocumentViewSet,
    base_name='bookdocument_frontend'
)

router.register(
    r'books-permissions',
    BookPermissionsDocumentViewSet,
    base_name='bookdocument_permissions'
)

router.register(
    r'books-custom',
    BookCustomDocumentViewSet,
    base_name='bookdocument_custom'
)

router.register(
    r'books-ignore-index-errors',
    BookIgnoreIndexErrorsDocumentViewSet,
    base_name='bookdocument_ignore_index_errors'
)

router.register(
    r'books-more-like-this',
    BookMoreLikeThisDocumentViewSet,
    base_name='bookdocument_more_like_this'
)

router.register(
    r'books-more-like-this-no-options',
    BookMoreLikeThisNoOptionsDocumentViewSet,
    base_name='bookdocument_more_like_this_no_options'
)

router.register(
    r'books-default-filter-lookup',
    BookDefaultFilterLookupDocumentViewSet,
    base_name='bookdocument_default_filter_lookup'
)

router.register(
    r'books-compound-search-backend',
    BookCompoundSearchBackendDocumentViewSet,
    base_name='bookdocument_compound_search_backend'
)

router.register(
    r'books-compound-search-boost-backend',
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    base_name='bookdocument_compound_search_boost_backend'
)

router.register(
    r'books-compound-search-backend-ordered-by-score',
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    base_name='bookdocument_compound_search_backend_ordered_by_score'
)

router.register(
    r'books-source',
    BookSourceSearchBackendDocumentViewSet,
    base_name='bookdocument_source'
)

router.register(
    r'books-multi-match-search-backend',
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    base_name='bookdocument_multi_match_search_backend'
)

router.register(
    r'books-multi-match-phrase-prefix-search-backend',
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    base_name='bookdocument_multi_match_phrase_prefix_search_backend'
)

router.register(
    r'books-simple-query-string-search-backend',
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    base_name='bookdocument_simple_query_string_search_backend'
)

router.register(
    r'books-simple-query-string-boost-search-backend',
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
    base_name='bookdocument_simple_query_string_boost_search_backend'
)

# **********************************************************
# ************************* Cities *************************
# **********************************************************

router.register(
    r'cities',
    CityDocumentViewSet,
    base_name='citydocument'
)

router.register(
    r'cities-compound-search-backend',
    CityCompoundSearchBackendDocumentViewSet,
    base_name='citydocument_compound_search_backend'
)

# **********************************************************
# *********************** Locations ************************
# **********************************************************

router.register(
    r'locations',
    LocationDocumentViewSet,
    base_name='locationdocument'
)

# **********************************************************
# *********************** Publishers ***********************
# **********************************************************

router.register(
    r'publishers',
    PublisherDocumentViewSet,
    base_name='publisherdocument'
)

# **********************************************************
# ********************** URL patterns **********************
# **********************************************************

urlpatterns = [
    url(r'^', include(router.urls)),
]
