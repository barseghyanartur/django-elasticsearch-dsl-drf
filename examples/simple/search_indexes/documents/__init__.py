from .address import AddressDocument
from .animal import AnimalDocument, ReadOnlyAnimalDocument
from .author import AuthorDocument
from .book import BookDocument
from .city import CityDocument
from .post import PostDocument
from .publisher import PublisherDocument
from .location import LocationDocument
from .tag import TagDocument
from .user import SiteUserDocument

__all___ = (
    'AddressDocument',
    'AuthorDocument',
    'AnimalDocument',
    'ReadOnlyAnimalDocument',
    'BookDocument',
    'CityDocument',
    'PostDocument',
    'PublisherDocument',
    'TagDocument',
    'SiteUserDocument',
)
