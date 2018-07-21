#!/usr/bin/env bash
cat README.rst docs/documentation.rst.distrib > docs/index.rst
cat CHANGELOG.rst > docs/changelog.rst
cat installing_elasticsearch.rst > docs/installing_elasticsearch.rst
cat search_backends.rst > docs/search_backends.rst
cat quick_start.rst > docs/quick_start.rst
cat basic_usage_examples.rst > docs/basic_usage_examples.rst
cat advanced_usage_examples.rst > docs/advanced_usage_examples.rst
cat nested_fields_usage_examples.rst > docs/nested_fields_usage_examples.rst
cat filtering_usage_examples.rst > docs/filtering_usage_examples.rst
cat misc_usage_examples.rst > docs/misc_usage_examples.rst
