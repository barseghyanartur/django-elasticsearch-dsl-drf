cat README.rst > docs/index.rst
sphinx-build -n -a -b html docs builddocs
sphinx-build -n -a -b pdf docs builddocs
cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..
