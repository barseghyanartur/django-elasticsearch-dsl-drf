Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: none

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.1.3
-----
2017-06-21

- Added tests for `more_like_this` helper, `range` filter and `prefix` filter.
- Minor documentation improvements.

0.1.2
-----
2017-06-20

- Minor fixes in tests.

0.1.1
-----
2017-06-20

- Fixes in `more_like_this` helper.
- Tiny documentation improvements.

0.1
---
2017-06-19

- Initial alpha release.
