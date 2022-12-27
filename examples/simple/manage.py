#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "OpenSearch")
    os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "Elasticsearch")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
