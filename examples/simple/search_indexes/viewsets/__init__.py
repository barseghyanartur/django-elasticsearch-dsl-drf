from .address import AddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookCompoundSearchBackendDocumentViewSet,
    BookCompoundSearchBoostSearchBackendDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookIgnoreIndexErrorsDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
    BookMoreLikeThisNoOptionsDocumentViewSet,
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
    BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet,
)
from .city import CityDocumentViewSet, CityCompoundSearchBackendDocumentViewSet
from .publisher import PublisherDocumentViewSet

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookCompoundSearchBackendDocumentViewSet',
    'BookCompoundSearchBoostSearchBackendDocumentViewSet',
    'BookDefaultFilterLookupDocumentViewSet',
    'BookDocumentViewSet',
    'BookFunctionalSuggesterDocumentViewSet',
    'BookIgnoreIndexErrorsDocumentViewSet',
    'BookMoreLikeThisDocumentViewSet',
    'BookMoreLikeThisNoOptionsDocumentViewSet',
    'BookMultiMatchSearchFilterBackendDocumentViewSet',
    'BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet',
    'BookOrderingByScoreCompoundSearchBackendDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'BookSimpleQueryStringSearchFilterBackendDocumentViewSet',
    'BookSimpleQueryStringBoostSearchFilterBackendDocumentViewSet',
    'CityCompoundSearchBackendDocumentViewSet',
    'CityDocumentViewSet',
    'PublisherDocumentViewSet',
)
