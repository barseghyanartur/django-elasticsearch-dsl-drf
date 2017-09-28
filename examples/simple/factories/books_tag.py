import random

from factory import DjangoModelFactory, LazyAttribute
from factory.fuzzy import FuzzyChoice

from books.models import Tag

from .constants import BOOK_GENRES
from .factory_faker import Faker

__all__ = (
    'TagFactory',
    'TagGenreFactory',
    'LimitedTagFactory',
)


class BaseTagFactory(DjangoModelFactory):
    """Base tag factory."""

    # Although the ``max_length`` of the of the ``title`` field of the
    # ``Tag`` model is set to 255, for usability we set this one to 20.
    title = Faker('catch_phrase')

    class Meta(object):
        """Meta class."""

        model = Tag
        abstract = True
        django_get_or_create = ('title',)


class TagFactory(BaseTagFactory):
    """Tag factory."""


class TagGenreFactory(BaseTagFactory):
    """Tag factory consisting of genres."""

    title = FuzzyChoice(BOOK_GENRES)

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('title',)


class LimitedTagFactory(BaseTagFactory):
    """Tag factory, but limited to 20 tags."""

    id = LazyAttribute(
        lambda __x: random.randint(1, 20)
    )

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)
