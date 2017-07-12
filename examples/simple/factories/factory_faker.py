# coding=utf-8

from __future__ import unicode_literals

from django.core.files.base import File

from factory import Faker as OriginalFaker

from faker import Faker as FakerFaker
from faker.providers import BaseProvider

from .files import get_temporary_file

__all__ = (
    'Faker',
    'DjangoFileProvider',
)


class Faker(OriginalFaker):
    """Override to change the default locale."""

    _DEFAULT_LOCALE = 'nl_NL'


class DjangoFileProvider(BaseProvider):
    """Django file provider."""

    @classmethod
    def django_file(cls, extension=None):
        """Generates a random file.

        Example:

        >>> from factory import DjangoModelFactory
        >>>
        >>> class ProductFactory(DjangoModelFactory):
        >>>     "Product factory."
        >>>
        >>>     # ...
        >>>
        >>>     image_file = Faker('django_file', extension='image')
        >>>     video_file = Faker('django_file', extension='video')
        >>>     text_file = Faker('django_file', extension='text')
        >>>
        >>>     # ...

        :param extension: File extension.
        :type extension: str
        :return: File object.
        """

        fake = FakerFaker()
        django_file = get_temporary_file(fake.file_name(extension=extension))
        return File(django_file)


Faker.add_provider(DjangoFileProvider)
