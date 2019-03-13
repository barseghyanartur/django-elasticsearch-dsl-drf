========================
Source filtering backend
========================
Allows to control how the `_source` field is returned with every hit.

By default operations return the contents of the _source field unless you have
used the `stored_fields` parameter or if the `_source` field is disabled.

You can turn off `_source` retrieval by using the `source` parameter:

.. code-block:: python

        from django_elasticsearch_dsl_drf.filter_backends import (
            SourceBackend
        )
        from django_elasticsearch_dsl_drf.viewsets import (
            BaseDocumentViewSet,
        )

        # Local article document definition
        from .documents import ArticleDocument

        # Local article document serializer
        from .serializers import ArticleDocumentSerializer

        class ArticleDocumentView(BaseDocumentViewSet):

            document = ArticleDocument
            serializer_class = ArticleDocumentSerializer
            filter_backends = [SourceBackend,]
            source = ["title"]


To disable `_source` retrieval set to False:

.. code-block:: python

        # ...
        source = False
        # ...


The `source` also accepts one or more wildcard patterns to control what parts
of the `_source` should be returned:

.. code-block:: python

        # ...
        source = ["title", "author.*"]
        # ...

Finally, for complete control, you can specify both `includes` and `excludes`
patterns:

.. code-block:: python

        # ...
        source = {
            "includes": ["title", "author.*"],
            "excludes": [ "*.description" ]
        }
        # ...

.. note::

    Source can make queries lighter. However, it can break current
    functionality. Use it with caution.
