Pagination
==========
Check the view definitions from the `advanced usage examples
<https://django-elasticsearch-dsl-drf.readthedocs.io/en/latest/advanced_usage_examples.html>`__.

Page number pagination
----------------------

By default, the ``PageNumberPagination`` class is used on all view sets
which inherit from ``DocumentViewSet``.

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?page=4
    http://127.0.0.1:8000/search/books/?page=4&page_size=100

Query friendly page number pagination
-------------------------------------

Works exactly as ``PageNumberPagination`` but fires (mostly) a single query to Elasticsearch,
instead of 2.

*search_indexes/viewsets/book.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.pagination import QueryFriendlyPageNumberPagination

    # ...

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        # ...

        pagination_class = QueryFriendlyPageNumberPagination

        # ...

Limit/offset pagination
-----------------------

In order to use a different ``pagination_class``, for instance the
``LimitOffsetPagination``, specify it explicitly in the view.

*search_indexes/viewsets/book.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination

    # ...

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        # ...

        pagination_class = LimitOffsetPagination

        # ...

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?limit=100
    http://127.0.0.1:8000/search/books/?offset=400&limit=100

Customisations
~~~~~~~~~~~~~~

If you want to add additional data to the paginated response, for instance,
the page size, subclass the correspondent pagination class and add your
modifications in the ``get_paginated_response_context`` method as follows:

.. code-block:: python

    from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


    class CustomPageNumberPagination(PageNumberPagination):
        """Custom page number pagination."""

        def get_paginated_response_context(self, data):
            __data = super(
                CustomPageNumberPagination,
                self
            ).get_paginated_response_context(data)
            __data.append(
                ('current_page', int(self.request.query_params.get('page', 1)))
            )
            __data.append(
                ('page_size', self.get_page_size(self.request))
            )

            return sorted(__data)

Same applies to the customisations of the ``LimitOffsetPagination``.
