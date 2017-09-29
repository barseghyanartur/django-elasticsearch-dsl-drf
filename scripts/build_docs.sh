#!/usr/bin/env bash
./scripts/prepare_docs.sh

sphinx-build -n -a -b html docs builddocs
sphinx-build -n -a -b pdf docs builddocs
cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..
