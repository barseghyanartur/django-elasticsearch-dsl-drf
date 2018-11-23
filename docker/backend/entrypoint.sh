#!/bin/sh

# Create dirs if necessary
echo "Creating dirs"
./scripts/create_dirs.sh

# Apply database migrations
echo "Apply database migrations"
./examples/simple/manage.py migrate --noinput --settings=settings.docker

# Create search index
echo "Create search index"
./examples/simple/manage.py search_index --rebuild -f --settings=settings.docker

# Start server
echo "Starting server"
python ./examples/simple/manage.py runserver 0.0.0.0:8000 --settings=settings.docker
