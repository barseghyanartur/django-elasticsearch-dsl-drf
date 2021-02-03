from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from books.models import Continent

from .factory_faker import Faker

__all__ = ('ContinentFactory',)


class BaseContinentFactory(DjangoModelFactory):
    """Base continent factory."""

    name = FuzzyChoice([
        'Asia',
        'Africa',
        'North America',
        'South America',
        'Antarctica',
        'Europe',
        'Australia'
    ])
    info = Faker('text')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

    class Meta(object):
        """Meta class."""

        model = Continent
        abstract = True
        django_get_or_create = ('name',)


class ContinentFactory(BaseContinentFactory):
    """Continent factory."""
