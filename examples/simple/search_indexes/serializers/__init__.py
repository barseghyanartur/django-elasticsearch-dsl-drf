from .address import (
    AddressDocumentSerializer,
    FrontendAddressDocumentSerializer,
)
from .author import AuthorDocumentSimpleSerializer
from .book import BookDocumentSerializer, BookDocumentSimpleSerializer
from .city import CityDocumentSerializer
from .publisher import (
    PublisherDocumentSerializer,
    PublisherDocumentSimpleSerializer,
)

__all__ = (
    'AddressDocumentSerializer',
    'AuthorDocumentSimpleSerializer',
    'BookDocumentSerializer',
    'BookDocumentSimpleSerializer',
    'CityDocumentSerializer',
    'FrontendAddressDocumentSerializer',
    'PublisherDocumentSerializer',
    'PublisherDocumentSimpleSerializer',
)
