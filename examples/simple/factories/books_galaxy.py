from factory import SubFactory
from factory.django import DjangoModelFactory

from books.models import Galaxy

from .factory_faker import Faker

__all__ = (
    'GalaxyFactory',
)


class BaseGalaxyFactory(DjangoModelFactory):
    """Base galaxy factory."""

    name = Faker('name')

    class Meta:
        """Meta class."""

        model = Galaxy
        abstract = True
        django_get_or_create = ('name',)


class GalaxyFactory(BaseGalaxyFactory):
    """Planet factory."""
