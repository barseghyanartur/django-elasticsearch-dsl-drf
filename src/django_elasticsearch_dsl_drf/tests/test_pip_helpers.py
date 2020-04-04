# -*- coding: utf-8 -*-
"""
Test pip_helpers.
"""

from __future__ import absolute_import, unicode_literals

import unittest

import django
import pytest

from ..pip_helpers import check_if_installed, get_installed_packages

__title__ = 'django_elasticsearch_dsl_drf.tests.test_pip_helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestPipHelpers',
)


@pytest.mark.django_db
class TestPipHelpers(unittest.TestCase):
    """Test pip_helpers."""

    @classmethod
    def setUpClass(cls):
        cls.mapping = {
            'country': {
                'name': 'Netherlands',
                'province': {
                    'name': 'North Holland',
                    'city': {
                        'name': 'Amsterdam',
                    }
                }
            }
        }

    def test_get_installed_packages(self):
        """Test `get_installed_packages`.

        :return:
        """
        installed_packages = get_installed_packages()
        self.assertIn('Django', installed_packages)
        self.assertIn('elasticsearch', installed_packages)
        self.assertIn('elasticsearch-dsl', installed_packages)

    def test_get_installed_packages_with_versions(self):
        """Test `get_installed_packages`.

        :return:
        """
        installed_packages = get_installed_packages(with_versions=True)
        django_version = django.get_version()
        self.assertIn(('Django', django_version), installed_packages)

    def test_check_if_installed(self):
        """Test `check_if_installed`.

        :return:
        """
        self.assertTrue(check_if_installed('Django'))
        self.assertTrue(check_if_installed('elasticsearch'))
        self.assertTrue(check_if_installed('elasticsearch-dsl'))
        self.assertFalse(check_if_installed('django-fobi'))
