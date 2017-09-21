=====================
Various handy helpers
=====================

Contents:

.. contents:: Table of Contents

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


Customize results as follows:

.. code-block:: python

    from django_elasticsearch_dsl_drf.helpers import more_like_this
    from elasticsearch_dsl.query import Q
    from books.models import Book
    book = Book.objects.first()
    query = Q('bool', must_not=Q('term', **{'state.raw': 'cancelled'}))
    similar_books = more_like_this(
        book,
        query=query,
        fields=['title', 'description', 'summary'],
        min_term_freq=2,
        min_doc_freq=1,
    )
