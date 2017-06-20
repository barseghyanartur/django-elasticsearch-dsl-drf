import random

from factory import DjangoModelFactory, LazyAttribute

from books.models import Author

from .factory_faker import Faker

__all__ = (
    'AuthorFactory',
    'LimitedAuthorFactory',
    'SingleAuthorFactory',
)


class BaseAuthorFactory(DjangoModelFactory):
    """Base author factory."""

    salutation = Faker('text', max_nb_chars=10)
    name = Faker('name')
    email = Faker('email')

    class Meta(object):
        """Meta class."""

        model = Author
        abstract = True


class AuthorFactory(BaseAuthorFactory):
    """Author factory."""


class LimitedAuthorFactory(BaseAuthorFactory):
    """Author factory, but limited to 20 authors."""

    id = LazyAttribute(
        lambda __x: random.randint(1, 20)
    )

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)


class SingleAuthorFactory(BaseAuthorFactory):
    """Author factory, limited to a single author."""

    id = 999999
    name = "Artur Barseghyan"
    email = "barseghyan@gw20e.com"

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)
