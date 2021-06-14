from .address import AddressDocument
from .author import AuthorDocument
from .book import BookDocument
from .city import CityDocument
from .journal import JournalDocument
from .location import LocationDocument
from .publisher import PublisherDocument
from .tag import TagDocument, NoKeywordTagDocument

__all___ = (
    'AddressDocument',
    'AuthorDocument',
    'BookDocument',
    'CityDocument',
    'PublisherDocument',
    'TagDocument',
    'NoKeywordTagDocument',
)
