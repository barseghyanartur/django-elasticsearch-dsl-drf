import random

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from books.models import Journal

from .factory_faker import Faker
from .constants import NON_FAKER_BOOK_CONTENT

__all__ = (
    'JournalChapter110Factory',
    'JournalChapter111Factory',
    'JournalChapter112Factory',
    'JournalChapter20Factory',
    'JournalChapter21Factory',
    'JournalChapter22Factory',
    'JournalChapter60Factory',
    'JournalChapter61Factory',
    'JournalChapter62Factory',
    'JournalFactory',
    'JournalWithUniqueTitleFactory',
)


class BaseJournalFactory(DjangoModelFactory):
    """Base journal factory."""

    isbn = Faker('isbn13')
    title = Faker('text', max_nb_chars=100)
    summary = Faker('text')
    publication_date = Faker('date_between', start_date='-10y', end_date='now')
    price = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    pages = LazyAttribute(
        lambda __x: random.randint(10, 200)
    )
    created = Faker('date_time')

    class Meta(object):
        """Meta class."""

        model = Journal
        abstract = True


class JournalFactory(BaseJournalFactory):
    """Journal factory."""


class JournalWithUniqueTitleFactory(BaseJournalFactory):
    """Journal factory with unique title attribute."""

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('title',)


# *************************************************************
# ****************** Factories with real texts ****************
# *************************************************************

# Second chapter, 3 times

class JournalChapter20Factory(JournalWithUniqueTitleFactory):
    """Journal chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[0]['title']
    summary = NON_FAKER_BOOK_CONTENT[0]['summary']
    description = NON_FAKER_BOOK_CONTENT[0]['description']


class JournalChapter21Factory(JournalWithUniqueTitleFactory):
    """Journal chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[1]['title']
    summary = NON_FAKER_BOOK_CONTENT[1]['summary']
    description = NON_FAKER_BOOK_CONTENT[1]['description']


class JournalChapter22Factory(JournalWithUniqueTitleFactory):
    """Journal chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[2]['title']
    summary = NON_FAKER_BOOK_CONTENT[2]['summary']
    description = NON_FAKER_BOOK_CONTENT[2]['description']


# Sixth chapter, 3 times

class JournalChapter60Factory(JournalWithUniqueTitleFactory):
    """Journal chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[3]['title']
    summary = NON_FAKER_BOOK_CONTENT[3]['summary']
    description = NON_FAKER_BOOK_CONTENT[3]['description']


class JournalChapter61Factory(JournalWithUniqueTitleFactory):
    """Journal chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[4]['title']
    summary = NON_FAKER_BOOK_CONTENT[4]['summary']
    description = NON_FAKER_BOOK_CONTENT[4]['description']


class JournalChapter62Factory(JournalWithUniqueTitleFactory):
    """Journal chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[5]['title']
    summary = NON_FAKER_BOOK_CONTENT[5]['summary']
    description = NON_FAKER_BOOK_CONTENT[5]['description']


# Eleventh chapter, 3 times

class JournalChapter110Factory(JournalWithUniqueTitleFactory):
    """Journal chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[6]['title']
    summary = NON_FAKER_BOOK_CONTENT[6]['summary']
    description = NON_FAKER_BOOK_CONTENT[6]['description']


class JournalChapter111Factory(JournalWithUniqueTitleFactory):
    """Journal chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[7]['title']
    summary = NON_FAKER_BOOK_CONTENT[7]['summary']
    description = NON_FAKER_BOOK_CONTENT[7]['description']


class JournalChapter112Factory(JournalWithUniqueTitleFactory):
    """Journal chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[8]['title']
    summary = NON_FAKER_BOOK_CONTENT[8]['summary']
    description = NON_FAKER_BOOK_CONTENT[8]['description']
