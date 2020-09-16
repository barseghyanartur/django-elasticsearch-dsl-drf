from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyChoice

from books.models import Galaxy

from .factory_faker import Faker

__all__ = (
    'GalaxyFactory',
)


class BaseGalaxyFactory(DjangoModelFactory):
    """Base galaxy factory."""

    name = Faker('name')

    class Meta(object):
        """Meta class."""

        model = Galaxy
        abstract = True
        django_get_or_create = ('name',)


class GalaxyFactory(BaseGalaxyFactory):
    """Planet factory."""
