from factory import DjangoModelFactory, SubFactory

from books.models import City

from .factory_faker import Faker

__all__ = ('CityFactory',)


class BaseCityFactory(DjangoModelFactory):
    """Base city factory."""

    name = Faker('city')
    info = Faker('text')
    country = SubFactory('factories.books_country.CountryFactory')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

    class Meta(object):
        """Meta class."""

        model = City
        abstract = True
        django_get_or_create = ('name',)


class CityFactory(BaseCityFactory):
    """City factory."""
