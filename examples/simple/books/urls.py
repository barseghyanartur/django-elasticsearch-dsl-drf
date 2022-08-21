from django.urls import re_path

from .views import (
    AddAuthorsToBookView,
    AuthorListView,
    AuthorListJSONView,
    AuthorListValuesView,
    AuthorListValuesWithCountsView,
    AuthorListWithCountsView,
    CreateAuthorsView,
    BookListView,
    BookListValuesView,
    BookListWithCountsView,
    PublisherIDsView,
    PublisherListView,
    UpdateBooksView,
    IndexView,
)

__all__ = ('urlpatterns',)


urlpatterns = [
    # Authors list
    re_path(r'^authors/$', AuthorListView.as_view(), name='books.authors'),

    # Authors list (more efficient)
    re_path(r'^authors-values/$',
        AuthorListValuesView.as_view(),
        name='books.authors_values'),

    # Authors list (with counts)
    re_path(r'^authors-with-counts/$',
        AuthorListWithCountsView.as_view(),
        name='books.authors_with_counts'),

    # Authors list (values with counts)
    re_path(r'^authors-values-with-counts/$',
        AuthorListValuesWithCountsView.as_view(),
        name='books.authors_values_with_counts'),

    # Authors list in JSON format
    re_path(r'^authors-json/$',
        AuthorListJSONView.as_view(),
        name='books.authors_json'),

    # Books list
    re_path(r'^books/$', BookListView.as_view(), name='books.books'),

    # Books list (with counts)
    re_path(r'^books-with-counts/$',
        BookListWithCountsView.as_view(),
        name='books.books_with_counts'),

    # Books list (more efficient)
    re_path(r'^books-values/$',
        view=BookListValuesView.as_view(),
        name='books.books_values'),

    # Publishers list
    re_path(r'^publishers/$',
        PublisherListView.as_view(),
        name='books.publishers'),

    # Publisher IDs
    re_path(r'^publisher-ids/$',
        PublisherIDsView.as_view(),
        name='books.publisher_ids'),

    # Create authors view
    re_path(r'^create-authors/$',
        CreateAuthorsView.as_view(),
        name='books.create_authors'),

    # Add authors to a book view
    re_path(r'^add-authors-to-book/$',
        AddAuthorsToBookView.as_view(),
        name='books.add_authors_to_book'),

    # Update books view
    re_path(r'^update-books/$',
        UpdateBooksView.as_view(),
        name='books.update_books'),

    # Index view
    re_path(r'^$', IndexView.as_view(), name='books.index'),
]
