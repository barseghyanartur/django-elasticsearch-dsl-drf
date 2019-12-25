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

0.20.4
------
2019-12-25

- Tested against Django 3.0.
- Tested against Python 3.8.
- Tested against Django REST Framework 3.11.
- Minor fixes.
- Test optimisations.

0.20.3
------
2019-09-20

- Testing the auxiliary versions module.

0.20.2
------
2019-08-30

- Minor improvements in test coverage.

0.20.1
------
2019-08-18

- Minor Elasticsearch 7.x compatibility fixes.

0.20
----
2019-08-17

- Adding Elasticsearch 7.x support.

0.19
----
2019-08-06

.. note::

    Dropping support for Elasticsearch versions prior 6.x. This is unfortunate,
    but this project depends on the upstream ``django-elasticsearch-dsl`` where
    as of version 6.4.x the support for older Elasticsearch versions was
    dropped. Use ``django-elasticsearch-dsl-drf`` version 0.18 if you need
    to work with 5.x or 2.x.

- Dropping support for Elasticsearch versions prior to 6.x.

0.18
----
2019-06-26

.. note::

    Support for Django versions prior 1.11 has been dropped.
    Support for Django REST Framework prior 3.9 has been dropped.

- Dropping support for Django versions prior 1.11.
- Dropping support for Django REST Framework versions prior 3.9.
- Fix Django REST Framework deprecations.

0.17.7
------
2019-05-30

.. note::

    Support for Django 1.8, 1.9 and 1.10 will be dropped in the next release.
    As usual, compatibility shims won't be removed directly. The change
    will affect the test matrix only first.

- Prevent unicode errors in tests on Python 2.7.
- Fixes in occasionally failing search test (``test_search`` and
  ``test_filtering_geo_spatial``).
- Working travis.
- Fixed issue with errors on empty ``ids`` filter.

0.17.6
------
2019-04-08

- Minor fixes.
- Additions to the docs.

0.17.5
------
2019-04-03

.. note::

    Dropping support for Python 3.4. As of this version everything works, but
    no longer tested.

- Minor fixes.
- Dropping Python 3.4 support.
- Django 2.2 support.

0.17.4
------
2019-03-13

- Source backend.

0.17.3
------
2019-02-08

- Obey object permissions.

0.17.2
------
2019-01-07

- Add nested ordering.

0.17.1
------
2018-12-12

- Skipping the new context suggester tests for Elasticsearch 2.x and a number
  of other 2.x related fixes in tests.
- A number of 5.x fixes in tests.

0.17
----
2018-12-12

.. note::

    Release supported by `whythawk <https://github.com/whythawk>`_.

- Added support for context suggesters (`category` and `geo`). Note, that
  this functionality is available for Elasticsearch 5.x and 6.x (thus, not
  for Elasticsearch 2.x).
- Added support for `size` attribute on suggesters.

0.16.3
------
2018-10-31

.. note::

    Release dedicated to Charles Aznavour.

- Make it possible to ignore certain Elastic exceptions by providing the
  appropriate ``ignore`` argument (on the view level). Default behaviour is
  intact. Set it to a list of integers (error codes) if you need it so.

0.16.2
------
2018-09-21

- Tested yet untested ``pip_helpers`` module.
- More tests.

0.16.1
------
2018-09-18

- Make it possible to control the size of the functional suggester queries.

0.16
----
2018-09-10

.. note::

    This release contains minor backwards incompatible changes. You might
    need to update your code if you have been making use of nested search.

*Old way of declaring nested search fields*

.. code-block:: python

    search_nested_fields = {
        'country': ['name'],
        'country.city': ['name'],
    }

*New way of declaring nested search fields*

.. code-block:: python

    search_nested_fields = {
        'country': {
            'path': 'country',
            'fields': ['name'],
        },
        'city': {
            'path': 'country.city',
            'fields': ['name'],
        },
    }

- Changes in nested search. This affects usage of both historical
  ``SearchFilterBackend`` and ``CompoundSearchFilterBackend``. Update your code
  accordingly.
- Take meta property ``using`` of the document ``Meta`` into consideration.

0.15.1
------
2018-08-22

- More tests.
- Fixes in docs.

0.15
----
2018-08-10

- Global aggregations.

0.14
----
2018-08-06

- More like this support through detail action.

0.13.2
------
2018-08-03

- Successfully tested against Python 3.7 and Django 2.1.
- Unified the base ``BaseSearchFilterBackend`` class.
- Minor clean up and fixes in docs.
- Upgrading test suite to modern versions (``pytest``, ``tox``,
  ``factory_boy``, ``Faker``). Removing unused dependencies from
  requirements (``drf-extensions``).
- Fixed missing PDF generation in offline documentation (non ReadTheDocs).
  The ``rst2pdf`` package (which does not support Python 3) has been replaced
  with ``rinohtype`` package (which does support Python 3).

0.13.1
------
2018-07-26

- Minor fix in suggesters on Elasticsearch 6.x.

0.13
----
2018-07-23

.. note::

    Release dedicated to Guido van Rossum, the former Python BDFL, who
    resigned from his BDFL position recently. Guido knew it better than we all
    do. His charisma, talent and leadership will be certainly missed a lot by
    the community. Thumbs up again for the best BDFL ever.

- The ``SimpleQueryStringSearchFilterBackend`` backend has been implemented.
- Minor fixes in the ``MultiMatchSearchFilterBackend`` backend.

0.12
----
2018-07-21

- New-style Search Filter Backends. Old style ``SearchFilterBackend`` is
  still supported (until at least version 0.16), but is deprecated. Migrate to
  ``CompoundSearchFilterBackend``. ``MultiMatchSearchFilterBackend``
  introduced (the name speaks for itself).
- From now on, your views would also work with model- and object-level
  permissions of the Django REST Framework (such as ``DjangoModelPermissions``,
  ``DjangoModelPermissionsOrAnonReadOnly`` and ``DjangoObjectPermissions``).
  Correspondent model or object would be used for that. If you find it
  incorrect in your case, write custom permissions and declare the explicitly
  in your view-sets.
- Fixed geo-spatial ``geo_distance`` ordering for Elastic 5.x. and 6.x.
- Fixes occasionally failing tests.

0.11
----
2018-07-15

.. note::

    This release contains backwards incompatible changes.
    You should update your Django code and front-end parts of your applications
    that were relying on the complex queries using ``|`` and ``:`` chars in the
    GET params.

.. note::

    If you have used custom filter backends using ``SEPARATOR_LOOKUP_VALUE``,
    ``SEPARATOR_LOOKUP_COMPLEX_VALUE`` or
    ``SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE`` constants or
    ``split_lookup_complex_value`` helper method of the ``FilterBackendMixin``,
    you most likely want to run your functional tests to see if everything
    still works.

.. note::

    Do not keep things as they were in your own fork, since new search backends
    will use the ``|`` and ``:`` symbols differently.

**Examples of old API requests vs new API requests**

.. note::

    Note, that ``|`` and ``:`` chars were mostly replaced with ``__`` and ``,``.

*Old API requests*

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name|reilly&search=city|london
    http://127.0.0.1:8000/search/publishers/?location__geo_distance=100000km|12.04|-63.93
    http://localhost:8000/api/articles/?id__terms=1|2|3
    http://localhost:8000/api/users/?age__range=16|67|2.0
    http://localhost:8000/api/articles/?id__in=1|2|3
    http://localhost:8000/api/articles/?location__geo_polygon=40,-70|30,-80|20,-90|_name:myname|validation_method:IGNORE_MALFORMED

*New API requests*

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name:reilly&search=city:london
    http://127.0.0.1:8000/search/publishers/?location__geo_distance=100000km__12.04__-63.93
    http://localhost:8000/api/articles/?id__terms=1__2__3
    http://localhost:8000/api/users/?age__range=16__67__2.0
    http://localhost:8000/api/articles/?id__in=1__2__3
    http://localhost:8000/api/articles/?location__geo_polygon=40,-70__30,-80__20,-90___name,myname__validation_method,IGNORE_MALFORMED

- ``SEPARATOR_LOOKUP_VALUE`` has been removed. Use
  ``SEPARATOR_LOOKUP_COMPLEX_VALUE`` and
  ``SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE`` instead.
- ``SEPARATOR_LOOKUP_NAME`` has been added.
- The method ``split_lookup_complex_value`` has been removed. Use
  ``split_lookup_complex_value`` instead.
- Default filter lookup option is added. In past, if no specific lookup was
  provided and there were multiple values for a single field to filter on, by
  default ``terms`` filter was used. The ``term`` lookup was used by default
  in similar situation for a single value to filter on. It's now possible to
  declare default lookup which will be used when no lookup is given.
- Removed deprecated ``views`` module. Import from ``viewsets`` instead.
- Removed undocumented ``get_count`` helper from ``helpers`` module.

0.10
----
2018-07-06

- Elasticsearch 6.x support.
- Minor fixes.

0.9
---
2018-07-04

- Introduced ``post_filter`` support.
- Generalised the ``FilteringFilterBackend`` backend. Both
  ``PostFilterFilteringFilterBackend`` and ``NestedFilteringFilterBackend``
  backends are now primarily based on it.
- Reduced Elastic queries from 3 to 2 when using ``LimitOffsetPagination``.

0.8.4
-----
2018-06-27

.. note::

    Release supported by `Goldmund, Wyldebeast & Wunderliebe
    <https://goldmund-wyldebeast-wunderliebe.nl/>`_.

- Added ``NestedFilteringFilterBackend`` backend.
- Documentation updated with examples of implementing a nested
  aggregations/facets.

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
