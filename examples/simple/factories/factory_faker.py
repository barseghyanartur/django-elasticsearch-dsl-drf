# coding=utf-8

from __future__ import unicode_literals

from factory import Faker as OriginalFaker

from faker import Faker as FakerFaker
from faker.providers import BaseProvider

__all__ = (
    'DjangoUserProvider',
    'EnGbFaker',
    'Faker',
    'NlNlFaker',
)


class NlNlFaker(OriginalFaker):
    """Override to change the default locale."""

    _DEFAULT_LOCALE = 'nl_NL'


Faker = NlNlFaker


class EnGbFaker(OriginalFaker):
    """Override to change the default locale."""

    _DEFAULT_LOCALE = 'en_GB'


class DjangoUserProvider(BaseProvider):
    """Django user provider."""
    _fake = FakerFaker()

    @classmethod
    def first_name_django(cls, max_length=30):
        """Generates first name compatible with django.

        Example:

        >>> from factory import DjangoModelFactory
        >>>
        >>> class UserFactory(DjangoModelFactory):
        >>>     "User factory."
        >>>
        >>>     # ...
        >>>
        >>>     image_file = Faker('first_name_django')
        >>>
        >>>     # ...

        :param max_length: Max length.
        :type max_length: int
        :return: str.
        """

        return cls._fake.first_name()[:max_length]

    @classmethod
    def last_name_django(cls, max_length=30):
        """Generates last name compatible with django.

        Example:

        >>> from factory import DjangoModelFactory
        >>>
        >>> class UserFactory(DjangoModelFactory):
        >>>     "User factory."
        >>>
        >>>     # ...
        >>>
        >>>     image_file = Faker('last_name_django')
        >>>
        >>>     # ...

        :param max_length: Max length.
        :type max_length: int
        :return: str.
        """

        return cls._fake.last_name()[:max_length]


Faker.add_provider(DjangoUserProvider)
