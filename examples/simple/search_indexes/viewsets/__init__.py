from .address import AddressDocumentViewSet, FrontAddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookCompoundSearchBackendDocumentViewSet,
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookCustomDocumentViewSet,
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
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    BookSourceSearchBackendDocumentViewSet,
)
from .city import CityDocumentViewSet, CityCompoundSearchBackendDocumentViewSet
from .location import LocationDocumentViewSet
from .post import PostDocumentViewSet
from .publisher import PublisherDocumentViewSet
from .tag import TagDocumentViewSet

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookCompoundSearchBackendDocumentViewSet',
    'BookCompoundSearchBoostSearchBackendDocumentViewSet',
    'BookDefaultFilterLookupDocumentViewSet',
    'BookDocumentViewSet',
    'BookCustomDocumentViewSet',
    'BookFrontendDocumentViewSet',
    'BookFunctionalSuggesterDocumentViewSet',
    'BookIgnoreIndexErrorsDocumentViewSet',
    'BookMoreLikeThisDocumentViewSet',
    'BookMoreLikeThisNoOptionsDocumentViewSet',
    'BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet',
    'BookMultiMatchSearchFilterBackendDocumentViewSet',
    'BookOrderingByScoreCompoundSearchBackendDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'BookPermissionsDocumentViewSet',
    'BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet',
    'BookSimpleQueryStringSearchFilterBackendDocumentViewSet',
    'BookSourceSearchBackendDocumentViewSet',
    'CityCompoundSearchBackendDocumentViewSet',
    'CityDocumentViewSet',
    'LocationDocumentViewSet',
    'PublisherDocumentViewSet',
    'PostDocumentViewSet',
    'FrontAddressDocumentViewSet',
    'TagDocumentViewSet',
)
