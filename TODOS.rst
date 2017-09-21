=====
TODOs
=====
Based on the MoSCoW principle. Must haves and should haves are planned to be
worked on.

* Features/issues marked with plus (+) are implemented/solved.
* Features/issues marked with minus (-) are yet to be implemented.

Must haves
==========
.. code-block:: text

    - Full support of all optional params of each native Elasticsearch filter,
      such as ``flags`` on ``regexp``.
    - Support ``mode`` argument in the ``OrderingFilterBackend``.
    - Think of making more-like-this a functional filter.
    - Add support for geo spatial search/filtering/ordering.
    - Document geo spatial filtering.
    - Improve documentation.
    - Implement faceted search filtering.
    + Skip suggestions functionality in all actions except the dedicated
      ``suggest`` action.
    + Add suggestions support (`term`, `phrase` and `completion`)
    + Add information about FacetedSearchFilter, faceted search, pagination.
    + Implement facets/aggregations.
    + Add pagination and faceted search tests.
    + Dynamic serializer for Document models.
    + Add tests for ``term`` filter.
    + Add tests for ``terms`` filter.
    + Add tests for ``range`` filter.
    + Add tests for ``exists`` filter.
    + Add tests for ``prefix`` filter.
    + Add tests for ``wildcard`` filter.
    + Add tests for ``ids`` filter.
    + Add tests for ``contains`` filter.
    + Add tests for ``in`` filter.
    + Add tests for ``gt`` filter.
    + Add tests for ``gte`` filter.
    + Add tests for ``lt`` filter.
    + Add tests for ``lte`` filter.
    + Add tests for ``startswith`` filter.
    + Add tests for ``endswith`` filter.
    + Add tests for ``isnull`` filter.
    + Add tests for ``exclude`` filter.
    + Implement ``term`` filter.
    + Implement ``terms`` filter.
    + Implement ``range`` filter.
    + Implement ``exists`` filter.
    + Implement ``prefix`` filter.
    + Implement ``wildcard`` filter.
    - Implement ``regexp`` filter.
    - Implement ``fuzzy`` filter.
    - Implement ``type`` filter.
    + Implement ``ids`` filter.
    + Implement ``contains`` filter.
    + Implement ``in`` filter.
    + Implement ``gt`` filter.
    + Implement ``gte`` filter.
    + Implement ``lt`` filter.
    + Implement ``lte`` filter.
    + Implement ``contains`` filter.
    + Implement ``startswith`` filter.
    + Implement ``endswith`` filter.
    + Implement ``isnull`` filter.
    + Implement ``exclude`` filter.
    + Make more-like-this shortcut more generic.

Should haves
============
.. code-block:: text


Could haves
===========
.. code-block:: text

    - Search in multiple indexes/documents.

Would haves
===========
.. code-block:: text
