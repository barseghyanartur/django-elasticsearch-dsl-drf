from .address import AddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookCompoundSearchBackendDocumentViewSet,
    BookDefaultFilterLookupDocumentViewSet,
    BookDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
    BookMultiMatchSearchFilterBackendDocumentViewSet,
    BookOrderingByScoreCompoundSearchBackendDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
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
    'BookOrderingByScoreCompoundSearchBackendDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'CityCompoundSearchBackendDocumentViewSet',
    'CityDocumentViewSet',
    'PublisherDocumentViewSet',
)
