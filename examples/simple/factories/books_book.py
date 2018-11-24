import random

from factory import (
    DjangoModelFactory,
    SubFactory,
    post_generation,
    LazyAttribute,
)
from factory.fuzzy import FuzzyChoice

from books.constants import BOOK_PUBLISHING_STATUS_CHOICES
from books.models import Book

from .factory_faker import Faker
from .books_author import (
    AuthorFactory,
    LimitedAuthorFactory,
    SingleAuthorFactory,
)
from .books_order import OrderFactory
from .books_orderline import OrderLineFactory
from .books_tag import LimitedTagFactory, TagFactory, TagGenreFactory
from .constants import NON_FAKER_BOOK_CONTENT

__all__ = (
    'BookChapterFactory',
    'BookChapter110Factory',
    'BookChapter111Factory',
    'BookChapter112Factory',
    'BookChapter20Factory',
    'BookChapter21Factory',
    'BookChapter22Factory',
    'BookChapter60Factory',
    'BookChapter61Factory',
    'BookChapter62Factory',
    'BookFactory',
    'BookNovelFactory',
    'BookWithoutOrdersFactory',
    'BookWithoutTagsAndOrdersFactory',
    'BookWithoutTagsFactory',
    'BookWithUniqueTitleFactory',
    'SingleBookFactory',
)


class BaseBookFactory(DjangoModelFactory):
    """Base book factory."""

    title = Faker('text', max_nb_chars=100)
    summary = Faker('text')
    publisher = SubFactory('factories.books_publisher.LimitedPublisherFactory')
    publication_date = Faker('date_between', start_date='-10y', end_date='now')
    price = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    isbn = Faker('isbn13')
    state = FuzzyChoice(dict(BOOK_PUBLISHING_STATUS_CHOICES).keys())
    pages = LazyAttribute(
        lambda __x: random.randint(10, 200)
    )
    created = Faker('date_time')

    class Meta(object):
        """Meta class."""

        model = Book
        abstract = True

    @post_generation
    def tags(obj, created, extracted, **kwargs):
        """Create Tag objects for the created Book instance."""
        if created:
            # Create from 1 to 7 ``Tag`` objects.
            amount = random.randint(1, 7)
            tags = TagGenreFactory.create_batch(amount, **kwargs)
            obj.tags.add(*tags)

    @post_generation
    def authors(obj, created, extracted, **kwargs):
        """Create `Author` objects for the created `Book` instance."""
        if created:
            # Create random amount of `Author` objects.
            amount = random.randint(3, 7)
            authors = LimitedAuthorFactory.create_batch(amount, **kwargs)
            obj.authors.add(*authors)

    @post_generation
    def orders(obj, created, extracted, **kwargs):
        """Create `Order` objects for the created `Book` instance."""
        if created:
            # Create 3 `Order` objects.
            amount = random.randint(2, 7)
            orders = OrderFactory.create_batch(amount, **kwargs)
            order_line_kwargs = dict(kwargs)
            order_line_kwargs['book'] = obj
            for order in orders:
                # Create 1 `OrderLine` object.
                amount = random.randint(1, 5)
                order_lines = OrderLineFactory.create_batch(
                    amount, **order_line_kwargs
                )
                order.lines.add(*order_lines)


class BookFactory(BaseBookFactory):
    """Book factory."""


class BookWithUniqueTitleFactory(BaseBookFactory):
    """Book factory with unique title attribute."""

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('title',)


class SingleBookFactory(BaseBookFactory):
    """Book factory, but limited to a single book."""

    id = 999999
    title = "Performance optimisation"
    publisher = SubFactory('factories.books_publisher.SinglePublisherFactory')

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)

    @post_generation
    def authors(obj, created, extracted, **kwargs):
        """Create `Author` objects for the created `Book` instance."""
        if created:
            # Create a single `Author` object.
            author = SingleAuthorFactory()
            obj.authors.add(author)


class BookWithoutTagsFactory(BaseBookFactory):
    """Book without tags factory."""

    @post_generation
    def tags(obj, created, extracted, **kwargs):
        """Dummy."""


class BookWithoutOrdersFactory(BaseBookFactory):
    """Book without orders factory."""

    @post_generation
    def orders(obj, created, extracted, **kwargs):
        """Dummy."""


class BookWithoutTagsAndOrdersFactory(BaseBookFactory):
    """Book without tags and orders factory."""

    @post_generation
    def tags(obj, created, extracted, **kwargs):
        """Dummy."""

    @post_generation
    def orders(obj, created, extracted, **kwargs):
        """Dummy."""


# *************************************************************
# ****************** Factories with real texts ****************
# *************************************************************

# Second chapter, 3 times

class BookChapterFactory(BookWithUniqueTitleFactory):
    """Book chapter factory."""

    @post_generation
    def tags(obj, created, extracted, **kwargs):
        """Create Tag objects for the created Book instance."""
        if created:
            # Create from 1 to 7 ``Tag`` objects.
            amount = random.randint(1, 7)
            tags = TagGenreFactory.create_batch(amount, **kwargs)
            tag = TagFactory(title='Alice')
            tags.append(tag)
            obj.tags.add(*tags)


class BookChapter20Factory(BookChapterFactory):
    """Book chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[0]['title']
    summary = NON_FAKER_BOOK_CONTENT[0]['summary']
    description = NON_FAKER_BOOK_CONTENT[0]['description']


class BookChapter21Factory(BookChapterFactory):
    """Book chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[1]['title']
    summary = NON_FAKER_BOOK_CONTENT[1]['summary']
    description = NON_FAKER_BOOK_CONTENT[1]['description']


class BookChapter22Factory(BookChapterFactory):
    """Book chapter II factory."""

    title = NON_FAKER_BOOK_CONTENT[2]['title']
    summary = NON_FAKER_BOOK_CONTENT[2]['summary']
    description = NON_FAKER_BOOK_CONTENT[2]['description']


# Sixth chapter, 3 times

class BookChapter60Factory(BookChapterFactory):
    """Book chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[3]['title']
    summary = NON_FAKER_BOOK_CONTENT[3]['summary']
    description = NON_FAKER_BOOK_CONTENT[3]['description']


class BookChapter61Factory(BookChapterFactory):
    """Book chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[4]['title']
    summary = NON_FAKER_BOOK_CONTENT[4]['summary']
    description = NON_FAKER_BOOK_CONTENT[4]['description']


class BookChapter62Factory(BookChapterFactory):
    """Book chapter VI factory."""

    title = NON_FAKER_BOOK_CONTENT[5]['title']
    summary = NON_FAKER_BOOK_CONTENT[5]['summary']
    description = NON_FAKER_BOOK_CONTENT[5]['description']


# Eleventh chapter, 3 times

class BookChapter110Factory(BookChapterFactory):
    """Book chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[6]['title']
    summary = NON_FAKER_BOOK_CONTENT[6]['summary']
    description = NON_FAKER_BOOK_CONTENT[6]['description']


class BookChapter111Factory(BookChapterFactory):
    """Book chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[7]['title']
    summary = NON_FAKER_BOOK_CONTENT[7]['summary']
    description = NON_FAKER_BOOK_CONTENT[7]['description']


class BookChapter112Factory(BookChapterFactory):
    """Book chapter XI factory."""

    title = NON_FAKER_BOOK_CONTENT[8]['title']
    summary = NON_FAKER_BOOK_CONTENT[8]['summary']
    description = NON_FAKER_BOOK_CONTENT[8]['description']

# Shekley books


class BookNovelFactory(BookWithUniqueTitleFactory):
    """Book novel factory - texts of Robert Sheckley."""

    @post_generation
    def tags(obj, created, extracted, **kwargs):
        """Create Tag objects for the created Book instance."""
        if created:
            # Create from 1 to 7 ``Tag`` objects.
            amount = random.randint(1, 7)
            tags = TagGenreFactory.create_batch(amount, **kwargs)
            tag = TagFactory(title='Sheckley')
            tags.append(tag)
            obj.tags.add(*tags)
