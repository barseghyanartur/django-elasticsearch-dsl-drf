from .address import AddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookCompoundSearchBackendDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet,
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet,
)
from .city import CityDocumentViewSet, CityCompoundSearchBackendDocumentViewSet
from .publisher import PublisherDocumentViewSet

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookCompoundSearchBackendDocumentViewSet',
    'BookDefaultFilterLookupDocumentViewSet',
    'BookDocumentViewSet',
    'BookFunctionalSuggesterDocumentViewSet',
    'BookMoreLikeThisDocumentViewSet',
    'BookMultiMatchSearchFilterBackendDocumentViewSet',
    'BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet',
    'BookOrderingByScoreCompoundSearchBackendDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'BookSimpleQueryStringSearchFilterBackendDocumentViewSet',
    'CityCompoundSearchBackendDocumentViewSet',
    'CityDocumentViewSet',
    'PublisherDocumentViewSet',
)
