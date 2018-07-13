from .address import AddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    BookMoreLikeThisDocumentViewSet,
)
from .city import CityDocumentViewSet
from .publisher import PublisherDocumentViewSet

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookDocumentViewSet',
    'BookFunctionalSuggesterDocumentViewSet',
    'BookMoreLikeThisDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'CityDocumentViewSet',
    'PublisherDocumentViewSet',
)
