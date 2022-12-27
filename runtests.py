#!/usr/bin/env python
import os
import sys

import pytest


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    # os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "OpenSearch")
    os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "Elasticsearch")
    sys.path.insert(0, "src")
    sys.path.insert(0, "examples/simple")
    return pytest.main()


if __name__ == '__main__':
    sys.exit(main())
