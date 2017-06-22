cat README.rst > docs/index.rst
cat BASIC_USAGE_EXAMPLES.rst > docs/basic_usage_examples.rst
cat ADVANCED_USAGE_EXAMPLES.rst > docs/advanced_usage_examples.rst
cat MISC_USAGE_EXAMPLES.rst > docs/misc_usage_examples.rst
sphinx-build -n -a -b html docs builddocs
sphinx-build -n -a -b pdf docs builddocs
cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..
