#!/usr/bin/env bash
cat README.rst docs/documentation.rst.distrib > docs/index.rst
cat CHANGELOG.rst > docs/changelog.rst
cat docs_src/installing_elasticsearch.rst > docs/installing_elasticsearch.rst
cat docs_src/search_backends.rst > docs/search_backends.rst
cat docs_src/quick_start.rst > docs/quick_start.rst
cat docs_src/basic_usage_examples.rst > docs/basic_usage_examples.rst
cat docs_src/advanced_usage_examples.rst > docs/advanced_usage_examples.rst
cat docs_src/nested_fields_usage_examples.rst > docs/nested_fields_usage_examples.rst
cat docs_src/filtering_usage_examples.rst > docs/filtering_usage_examples.rst
cat docs_src/more_like_this.rst > docs/more_like_this.rst
cat docs_src/source_backend.rst > docs/source_backend.rst
cat docs_src/configuration_tweaks.rst > docs/configuration_tweaks.rst
cat docs_src/global_aggregations.rst > docs/global_aggregations.rst
cat examples/frontend/README.rst > docs/frontend_demo.rst
