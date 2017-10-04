from factory import DjangoModelFactory, SubFactory

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

    class Meta(object):
        """Meta class."""

        model = Address
        abstract = True


class AddressFactory(BaseAddressFactory):
    """Address factory."""
