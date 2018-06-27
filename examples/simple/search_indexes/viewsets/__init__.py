from .address import AddressDocumentViewSet
from .author import AuthorDocumentViewSet
from .book import (
    BookDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
)
from .city import CityDocumentViewSet
from .publisher import PublisherDocumentViewSet

__all__ = (
    'AddressDocumentViewSet',
    'AuthorDocumentViewSet',
    'BookDocumentViewSet',
    'BookOrderingByScoreDocumentViewSet',
    'CityDocumentViewSet',
    'PublisherDocumentViewSet',
)
