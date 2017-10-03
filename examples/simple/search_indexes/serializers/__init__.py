from .address import AddressDocumentSerializer
from .author import AuthorDocumentSimpleSerializer
from .book import BookDocumentSerializer, BookDocumentSimpleSerializer
from .publisher import (
    PublisherDocumentSerializer,
    PublisherDocumentSimpleSerializer,
)

__all__ = (
    'AuthorDocumentSimpleSerializer',
    'BookDocumentSerializer',
    'BookDocumentSimpleSerializer',
    'PublisherDocumentSerializer',
    'PublisherDocumentSimpleSerializer',
)
