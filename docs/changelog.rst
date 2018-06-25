Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.8.3
-----
2018-06-25

- It's possible to retrieve original dictionary from ``DictionaryProxy``
  object.
- Added helper wrappers and helper functions as a temporary fix for issues
  in the ``django-elasticsearch-dsl``.

0.8.2
-----
2018-06-05

- Minor fixes.

0.8.1
-----
2018-06-05

- Fixed wrong filter name in functional suggesters results into an error on
  Django 1.10 (and prior).
- Documentation improvements.

0.8
---
2018-06-01

.. note::

    Release supported by `Goldmund, Wyldebeast & Wunderliebe
    <https://goldmund-wyldebeast-wunderliebe.nl/>`_.

.. note::

    This release contain minor backwards incompatible changes. You should
    update your code.

    - (1) ``BaseDocumentViewSet`` (which from now on does not contain
          ``suggest`` functionality) has been renamed to ``DocumentViewSet``
          (which does contain ``suggest`` functionality).
    - (2) You should no longer import from
          ``django_elasticsearch_dsl_drf.views``. Instead, import from
          ``django_elasticsearch_dsl_drf.viewsets``.

- Deprecated ``django_elasticsearch_dsl_drf.views`` in favour
  of ``django_elasticsearch_dsl_drf.viewsets``.
- Suggest action/method has been moved to ``SuggestMixin`` class.
- ``FunctionalSuggestMixin`` class introduced which resembled functionality
  of the ``SuggestMixin`` with several improvements/additions, such as
  advanced filtering and context-aware suggestions.
- You can now define a default suggester in ``suggester_fields`` which will
  be used if you do not provide suffix for the filter name.

0.7.2
-----
2018-05-09

.. note::

    Release dedicated to the Victory Day, the victims of the Second World War
    and Liberation of Shushi.

- Django REST framework 3.8.x support.

0.7.1
-----
2018-04-04

.. note::

    Release supported by `Goldmund, Wyldebeast & Wunderliebe
    <https://goldmund-wyldebeast-wunderliebe.nl/>`_.

- Add query `boost` support for search fields.

0.7
---
2018-03-08

.. note::

    Dear ladies, congratulations on `International Women's Day
    <https://en.wikipedia.org/wiki/International_Women%27s_Day>`_

- CoreAPI/CoreSchema support.

0.6.4
-----
2018-03-05

- Minor fix: explicitly use DocType in the ViewSets.

0.6.3
-----
2018-01-03

- Minor fix in the search backend.
- Update the year in the license and code.

0.6.2
-----
2017-12-29

- Update example project (and the tests that are dependant on the example
  project) to work with Django 2.0.
- Set minimal requirement for ``django-elasticsearch-dsl`` to 3.0.

0.6.1
-----
2017-11-28

- Documentation fixes.

0.6
---
2017-11-28

- Added highlight backend.
- Added nested search functionality.

0.5.1
-----
2017-10-18

- Fixed serialization of complex nested structures (lists of nested objects).
- Documentation fixes.

0.5
---
2017-10-05

.. note::

    This release contains changes that might be backwards incompatible
    for your project. If you have used dynamic document serializer
    ``django_elasticsearch_dsl_drf.serializers.DocumentSerializer``
    with customisations (with use of ``serializers.SerializerMethodField``,
    having the value parsed to JSON), just remove the custom parts.

- Support for ``ObjectField``, ``NestedField``, ``GeoPointField``,
  ``ListField``, ``GeoShapeField`` (and in general, nesting fields either
  as a dictionary or list should not be a problem at all).
- Dynamic serializer has been made less strict.
- Added ``get_paginated_response_context`` methods to both
  ``PageNumberPagination`` and ``LimitOffsetPagination`` pagination classes
  to simplify customisations.

0.4.4
-----
2017-10-02

- Documentation improvements (Elasticsearch suggestions).
- More tests (term and phrase suggestions).
- Code style fixes.

0.4.3
-----
2017-09-28

- Documentation fixes.
- Fixes in tests.
- Improved factories.

0.4.2
-----
2017-09-28

- Added ``geo_bounding_box`` query support to the geo-spatial features.

0.4.1
-----
2017-09-26

- Fixes in docs.

0.4
---
2017-09-26

.. note::

    This release contains changes that might be backwards incompatible
    for your project. Make sure to add the ``DefaultOrderingFilterBackend``
    everywhere you have used the ``OrderingFilterBackend``, right after the
    latter.

- ``GeoSpatialFilteringFilterBackend`` filtering backend, supporting
  ``geo_distance`` and ``geo_polygon`` geo-spatial queries.
- ``GeoSpatialOrderingFilterBackend`` ordering backend, supporting
  ordering of results for ``geo_distance`` filter.
- ``OrderingFilterBackend`` no longer provides defaults when no ordering is
  given. In order to take care of the defaults include the
  ``DefaultOrderingFilterBackend`` in the list of ``filter_backends`` (after
  all other ordering backends).

0.3.12
------
2017-09-21

- Added ``geo_distance`` filter. Note, that although functionally the filter
  would not change its' behaviour, it is likely to be moved to a separate
  backend (``geo_spatial``). For now use as is.
- Minor fixes.

0.3.11
------
2017-09-21

- Added ``query`` argument to ``more_like_this`` helper.

0.3.10
------
2017-09-20

- Minor fixes.
- Simplified Elasticsearch version check.

0.3.9
-----
2017-09-12

- Python 2.x compatibility fix.

0.3.8
-----
2017-09-12

- Fixes tests on some environments.

0.3.7
-----
2017-09-07

- Docs fixes.

0.3.6
-----
2017-09-07

- Fixed suggestions test for Elasticsearch 5.x.
- Added `compat` module for painless testing of Elastic 2.x to Elastic 5.x
  transition.

0.3.5
-----
2017-08-24

- Minor fixes in the ordering backend.
- Improved tests and coverage.

0.3.4
-----
2017-08-23

- Minor fixes in the ordering backend.

0.3.3
-----
2017-07-13

- Minor fixes and improvements.

0.3.2
-----
2017-07-12

- Minor fixes and improvements.

0.3.1
-----
2017-07-12

- Minor Python2 fixes.
- Minor documentation fixes.

0.3
---
2017-07-11

- Add suggestions support (``term``, ``phrase`` and ``completion``).

0.2.6
-----
2017-07-11

- Minor fixes.
- Fixes in documentation.

0.2.5
-----
2017-07-11

- Fixes in documentation.

0.2.4
-----
2017-07-11

- Fixes in documentation.

0.2.3
-----
2017-07-11

- Fixes in documentation.

0.2.2
-----
2017-07-11

- Fixes in documentation.

0.2.1
-----
2017-07-11

- Fixes in documentation.

0.2
---
2017-07-11

- Initial faceted search support.
- Pagination support.

0.1.8
-----
2017-06-26

- Python2 fixes.
- Documentation and example project improvements.

0.1.7
-----
2017-06-25

- Dynamic serializer for Documents.
- Major improvements in documentation.

0.1.6
-----
2017-06-23

- Implemented ``gt``, ``gte``, ``lt`` and ``lte`` functional query lookups.
- Implemented ``ids`` native filter lookup.

0.1.5
-----
2017-06-22

- Implemented ``endswith`` and ``contains`` functional filters.
- Added tests for ``wildcard``, ``exists``, ``exclude`` and ``isnull`` filters.
  Improved ``range`` filter tests.
- Improve ``more_like_this`` helper test.
- Improve ordering tests.
- Two additional arguments added to the ``more_like_this`` helper:
  ``min_doc_freq`` and ``max_doc_freq``.
- Minor documentation improvements.

0.1.4
-----
2017-06-22

- Added tests for ``in``, ``term`` and ``terms`` filters.
- Minor documentation fixes.

0.1.3
-----
2017-06-21

- Added tests for ``more_like_this`` helper, ``range`` and ``prefix`` filters.
- Minor documentation improvements.

0.1.2
-----
2017-06-20

- Minor fixes in tests.

0.1.1
-----
2017-06-20

- Fixes in ``more_like_this`` helper.
- Tiny documentation improvements.

0.1
---
2017-06-19

- Initial beta release.
