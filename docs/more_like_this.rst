==============
More like this
==============
More like this functionality.

Usage example
=============

Sample view
-----------

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends import (
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        PostFilterFilteringFilterBackend,
        SearchFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import (
        DocumentViewSet,
        MoreLikeThisMixin,
    )

    class BookMoreLikeThisDocumentViewSet(DocumentViewSet,
                                          MoreLikeThisMixin):
        """Same as BookDocumentViewSet, with more-like-this and no facets."""

        filter_backends = [
            # ...
            FilteringFilterBackend,
            PostFilterFilteringFilterBackend,
            IdsFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
            # ...
        ]

        # More-like-this options
        more_like_this_options = {
            'fields': (
                'title.mlt',
                'summary.mlt',
                'description.mlt',
            )
        }

Sample request
--------------

.. code-block:: text

    http://localhost:8000/search/books-more-like-this-no-options/1007587/more_like_this/

Generated query
---------------

.. code-block:: javascript

    {
      "query": {
        "more_like_this": {
          "fields": [
            "title.mlt",
            "summary.mlt",
            "description.mlt"
          ],
          "like": {
            "_index": "book",
            "_id": "1007587",
            "_type": "book_document"
          }
        }
      },
      "from": 0,
      "size": 14,
      "sort": [
        "_score"
      ]
    }

Options
-------
Pretty much `all Elasticsearch more-like-this options
<https://www.elastic.co/guide/en/elasticsearch/reference/5.5/query-dsl-mlt-query.html>`_
available. You might be particularly interested in the
following:

- min_term_freq
- max_query_terms
- unlike
- stop_words
