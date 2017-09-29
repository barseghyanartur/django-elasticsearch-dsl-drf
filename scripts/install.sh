#!/usr/bin/env bash
pip install -r examples/requirements/dev.txt
python setup.py develop
mkdir -p examples/logs examples/db examples/media examples/media/static
python examples/simple/manage.py collectstatic --noinput
python examples/simple/manage.py migrate --noinput
