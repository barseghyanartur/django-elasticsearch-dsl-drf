from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from books.models import City

from .factory_faker import Faker

__all__ = (
    'CityFactory',
    'DutchCityFactory',
    'SwissCityFactory',
    'DUTCH_CITIES',
    'SWISS_CITIES',
)


class BaseCityFactory(DjangoModelFactory):
    """Base city factory."""

    name = Faker('city')
    info = Faker('text')
    country = SubFactory('factories.books_country.CountryFactory')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

    class Meta:
        """Meta class."""

        model = City
        abstract = True
        django_get_or_create = ('name',)


class CityFactory(BaseCityFactory):
    """City factory."""


# 20 Dutch cities. The idea behind this is that some city names are common
# for Dutch and Swiss. Therefore, it's not really possible to randomly
# create unique results. Thus, doing it this way (always work).
DUTCH_CITIES = (
    'Amsterdam',
    'Anna Paulowna',
    'Annen',
    'Annerveenschekanaal',
    'Ansen',
    'Apeldoorn',
    'Appelscha',
    'Appeltern',
    'Appingedam',
    'Arcen',
    'Berltsum',
    'Best',
    'Beugen',
    'Beuningen Gld',
    'Beuningen',
    'Beusichem',
    'Beutenaken',
    'Darp',
    'Eindhoven',
    'Groningen',
)


class DutchCityFactory(BaseCityFactory):
    """Dutch city factory.

    You can safely say factories.DutchCityFactory.create_batch(100) and
    be sure that only 20 would be created.
    """

    name = FuzzyChoice(DUTCH_CITIES)

    class Meta:
        """Meta class."""

        model = City
        django_get_or_create = ('name',)


# 10 Swiss cities. See the remark for `DUTCH_CITIES`.
SWISS_CITIES = (
    'Basel',
    'Bern',
    'Biel/Bienne',
    'Geneva',
    'Lausanne',
    'Lucerne',
    'Lugano',
    'St. Gallen',
    'Winterthur',
    'Zurich',
)


class SwissCityFactory(BaseCityFactory):
    """Swiss city factory.

    You can safely say factories.SwissCityFactory.create_batch(100) and
    be sure that only 10 would be created.
    """

    name = FuzzyChoice(SWISS_CITIES)

    class Meta:
        """Meta class."""

        model = City
        django_get_or_create = ('name',)
