from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyChoice

from books.models import Location
from books.constants import LOCATION_CATEGORY_CHOICES

from .factory_faker import EnGbFaker as Faker

__all__ = ('LocationFactory',)


class BaseLocationFactory(DjangoModelFactory):
    """Base location factory."""

    group = FuzzyChoice([_choice[0] for _choice in LOCATION_CATEGORY_CHOICES])
    occupation_status = Faker('pybool')
    postcode = Faker('postcode')
    address_no = Faker('pyint')
    address_street = Faker('street_name')
    address_town = Faker('city')
    authority_name = Faker('company')
    # geocode = Faker('postcode')
    slug = Faker('uuid4')
    floor_area = Faker('pyfloat')
    employee_count = Faker('pyfloat')
    rental_valuation = Faker('pyfloat')
    revenue = Faker('pyfloat')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

    class Meta(object):
        """Meta class."""

        model = Location
        abstract = True
        django_get_or_create = ('slug',)


class LocationFactory(BaseLocationFactory):
    """Location factory."""
