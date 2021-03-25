from .address import *
from .author import *
from .book import *
from .city import *
from .journal import *
from .location import *
from .publisher import *
from .tag import *

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookCompoundFuzzySearchBackendDocumentViewSet',
    'BookCompoundSearchBackendDocumentViewSet',
    'BookCompoundSearchBoostSearchBackendDocumentViewSet',
    'BookCustomDocumentViewSet',
    'BookDefaultFilterLookupDocumentViewSet',
    'BookDocumentViewSet',
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
    'BookNoPermissionsDocumentViewSet',
    'BookNoRecordsDocumentViewSet',
    'BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet',
    'BookSimpleQueryStringSearchFilterBackendDocumentViewSet',
    'BookSourceSearchBackendDocumentViewSet',
    'CityCompoundSearchBackendDocumentViewSet',
    'CityDocumentViewSet',
    'JournalDocumentViewSet',
    'FrontAddressDocumentViewSet',
    'LocationDocumentViewSet',
    'PublisherDocumentViewSet',
    'QueryFriendlyPaginationBookDocumentViewSet',
    'TagDocumentViewSet',
)
