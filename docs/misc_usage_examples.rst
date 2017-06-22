=====================
Various handy helpers
=====================

More like this
==============

To get more-like-this results on a random registered model, do as follows:

.. code-block:: python

    from django_elasticsearch_dsl_drf.helpers import more_like_this
    from books.models import Book
    book = Book.objects.first()
    similar_books = more_like_this(
        book,
        ['title', 'description', 'summary']
    )
