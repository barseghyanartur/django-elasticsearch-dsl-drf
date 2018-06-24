from factory import DjangoModelFactory, SubFactory

from books.models import Country

from .factory_faker import Faker

__all__ = ('CountryFactory',)


class BaseCountryFactory(DjangoModelFactory):
    """Base country factory."""

    name = Faker('country')
    info = Faker('text')
    continent = SubFactory('factories.books_continent.ContinentFactory')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

    class Meta(object):
        """Meta class."""

        model = Country
        abstract = True
        django_get_or_create = ('name',)


class CountryFactory(BaseCountryFactory):
    """Country factory."""
