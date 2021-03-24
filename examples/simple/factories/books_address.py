from factory import SubFactory
from factory.django import DjangoModelFactory

from books.models import Address

from .factory_faker import Faker

__all__ = ('AddressFactory',)


class BaseAddressFactory(DjangoModelFactory):
    """Base address factory."""

    street = Faker('street_name')
    house_number = Faker('building_number')
    zip_code = Faker('postcode')
    city = SubFactory('factories.books_city.CityFactory')
    latitude = Faker('latitude')
    longitude = Faker('longitude')
    planet = SubFactory('factories.books_planet.PlanetFactory')

    class Meta:
        """Meta class."""

        model = Address
        abstract = True


class AddressFactory(BaseAddressFactory):
    """Address factory."""
