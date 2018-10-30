====================
Configuration tweaks
====================
Ignore certain Elasticsearch exceptions
---------------------------------------
.. code-block:: python

    class BookIgnoreIndexErrorsDocumentViewSet(DocumentViewSet):

        # ...
        ignore = [404]
        # ...
