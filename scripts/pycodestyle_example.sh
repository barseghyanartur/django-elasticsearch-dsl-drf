#!/usr/bin/env bash
reset
pycodestyle examples/simple/ --exclude examples/simple/wsgi.py,examples/simple/books/migrations/,examples/simple/books/tests/,
