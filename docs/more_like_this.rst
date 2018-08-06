==============
More like this
==============
More like this functionality.

Usage example
=============
Sample document
---------------

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import DocType, Index, fields
    from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
    from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion

    from books.models import Book

    from .analyzers import html_strip

    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1,
        blocks={'read_only_allow_delete': False}
    )


    @INDEX.doc_type
    class BookDocument(DocType):

        # ID
        id = fields.IntegerField(attr='id')

        title = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
                'edge_ngram_completion': StringField(
                    analyzer=edge_ngram_completion
                ),
                'mlt': StringField(analyzer='english'),
            }
        )

        description = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'mlt': StringField(analyzer='english'),
            }
        )

        summary = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'mlt': StringField(analyzer='english'),
            }
        )

        # ...

        class Meta(object):
            """Meta options."""

            model = Book  # The model associate with this DocType

        def prepare_summary(self, instance):
            """Prepare summary."""
            return instance.summary[:32766]

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

    from .serializers import BookDocumentSerializer

    class BookMoreLikeThisDocumentViewSet(DocumentViewSet,
                                          MoreLikeThisMixin):
        """Same as BookDocumentViewSet, with more-like-this and no facets."""

        # ...

        document = BookDocument
        lookup_field = 'id'
        serializer_class = BookDocumentSerializer

        # ...

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
