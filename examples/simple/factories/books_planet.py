from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyChoice

from books.models import Planet

from .factory_faker import Faker

__all__ = (
    'PlanetFactory',
)


class BasePlanetFactory(DjangoModelFactory):
    """Base planet factory."""

    name = Faker('name')

    class Meta(object):
        """Meta class."""

        model = Planet
        abstract = True
        django_get_or_create = ('name',)


class PlanetFactory(BasePlanetFactory):
    """Planet factory."""
