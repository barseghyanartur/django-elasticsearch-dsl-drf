from django.views.generic import ListView, TemplateView
from django.db.models import Avg, Count, DecimalField, F, Max, Min, Sum

from ormex.aggregations import GroupConcat

import factories

from .mixins import JSONResponseMixin
from .models import Author, Book, Publisher


__all__ = (
    'AddAuthorsToBookView',
    'AuthorListView',
    'AuthorListJSONView',
    'AuthorListValuesView',
    'AuthorListValuesWithCountsView',
    'AuthorListWithCountsView',
    'CreateAuthorsView',
    'BookListView',
    'BookListValuesView',
    # 'OrderLineListView',
    # 'OrderListView',
    'PublisherIDsView',
    'PublisherListView',
    'UpdateBooksView',
    'IndexView',
)


class IndexView(TemplateView):
    """Index."""

    template_name = 'books/index.html'


class PublisherListView(ListView):
    """Publishers."""

    model = Publisher


class BookListView(ListView):
    """Books."""

    model = Book

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .select_related('publisher') \
            .prefetch_related('authors') \
            .only('id',
                  'title',
                  'pages',
                  'price',
                  'publisher__id',
                  'publisher__name',
                  'authors__id',
                  'authors__name')


class BookListWithCountsView(ListView):
    """Books list with counts."""

    model = Book
    template_name = 'books/book_list_with_counts.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .select_related('publisher') \
            .prefetch_related('authors') \
            .only('id',
                  'title',
                  'pages',
                  'price',
                  'publisher__id',
                  'publisher__name',
                  'authors__id',
                  'authors__name') \
            .annotate(
                price_per_page=Sum(
                    F('price') / F('pages'),
                    output_field=DecimalField(decimal_places=2)
                )
            )


class BookListValuesView(ListView):
    """Books."""

    model = Book
    template_name = 'books/book_list_values.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .values('id',
                    'title',
                    'pages',
                    'price',
                    'publisher__id',
                    'publisher__name') \
            .annotate(
                authors__name=GroupConcat('authors__name', separator=', ')
            ) \
            .distinct()


class AuthorListView(ListView):
    """Authors."""

    model = Author


class AuthorListWithCountsView(ListView):
    """Authors list with counts."""

    model = Author
    template_name = 'books/author_list_with_counts.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .only('id',
                  'salutation',
                  'name',
                  'email') \
            .annotate(
                number_of_books=Count('books'),
                first_book_published_on=Min('books__publication_date'),
                last_book_published_on=Max('books__publication_date'),
                lowest_book_price=Min('books__price'),
                highest_book_price=Max('books__price'),
                average_book_price=Avg('books__price'),
                average_number_of_pages_per_book=Avg('books__pages'),
                number_of_books_sold=Count('books__order_lines'),
                total_amount_earned=Sum(
                    'books__order_lines__book__price'
                )
            )


class AuthorListValuesView(ListView):
    """Authors list (using ``values``)."""

    model = Author
    template_name = 'books/author_list_values.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .values('id',
                    'salutation',
                    'name',
                    'email')


class AuthorListValuesWithCountsView(ListView):
    """Authors list (using ``values``) with counts."""

    model = Author
    template_name = 'books/author_list_values_with_counts.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all() \
            .annotate(
                number_of_books=Count('books'),
                first_book_published_on=Min('books__publication_date'),
                last_book_published_on=Max('books__publication_date'),
                lowest_book_price=Min('books__price'),
                highest_book_price=Max('books__price'),
                average_book_price=Avg('books__price'),
                average_number_of_pages_per_book=Avg('books__pages'),
                number_of_books_sold=Count('books__order_lines'),
                total_amount_earned=Sum('books__order_lines__book__price')
            ) \
            .values('id',
                    'salutation',
                    'name',
                    'email',
                    'number_of_books',
                    'first_book_published_on',
                    'last_book_published_on',
                    'lowest_book_price',
                    'highest_book_price',
                    'average_book_price',
                    'average_number_of_pages_per_book',
                    'number_of_books_sold',
                    'total_amount_earned')


class AuthorListJSONView(JSONResponseMixin, TemplateView):
    """Authors list JSON response."""

    model = Author

    def get_data(self, context):
        """Get queryset."""
        return list(
            self.model.objects.all()
                .values('id',
                        'salutation',
                        'name',
                        'email')
        )

    def render_to_response(self, context, **response_kwargs):
        """Render."""
        response_kwargs.update({'safe': False})

        return self.render_to_json_response(context, **response_kwargs)


class CreateAuthorsView(TemplateView):
    """Create authors view."""

    template_name = 'books/create_authors.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        authors_list = []
        for __i in range(1, 50):
            author = factories.AuthorFactory.build()
            authors_list.append(author)

        Author.objects.bulk_create(authors_list)

        return {'object_list': authors_list}


class AddAuthorsToBookView(TemplateView):
    """Add authors to a book view."""

    template_name = 'books/add_authors_to_book.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        book = Book.objects.select_related('publisher').first()

        authors = Author.objects.filter()[:50]

        book.authors.add(*authors)

        return {'object_list': [book], 'book_authors': authors}


class PublisherIDsView(TemplateView):
    """List of Publisher IDs."""

    template_name = 'books/publisher_ids.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        books = Book.objects.filter()[:50]

        publisher_ids = [__b.publisher_id for __b in books]

        return {'object_list': publisher_ids}


class UpdateBooksView(TemplateView):
    """Update books view.."""

    template_name = 'books/update_books.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        # Just get some book IDs.
        book_ids = Book.objects.values_list('id', flat=True)[:50]

        books = Book.objects \
            .filter(id__in=book_ids) \
            .update(stock_count=F('stock_count') - 1)

        return {'number_of_books_updated': books}
