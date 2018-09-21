# -*- coding: utf-8 -*-
"""
Test wrappers.
"""

from __future__ import absolute_import, unicode_literals

import json
import unittest

import pytest

from ..wrappers import obj_to_dict, dict_to_obj

__title__ = 'django_elasticsearch_dsl_drf.tests.test_wrappers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestWrappers',
)


@pytest.mark.django_db
class TestWrappers(unittest.TestCase):
    """Test wrappers."""

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

    def test_obj_to_dict(self):
        """Test `obj_to_dict`.

        :return:
        """
        wrapper = dict_to_obj(self.mapping)
        self.assertEqual(
            wrapper.country.name,
            self.mapping['country']['name']
        )

        self.assertEqual(
            wrapper.country.province.name,
            self.mapping['country']['province']['name']
        )

        self.assertEqual(
            wrapper.country.province.city.name,
            self.mapping['country']['province']['city']['name']
        )

        # See if original ``mapping`` is same as ``as_dict``
        self.assertEqual(
            wrapper.as_dict,
            self.mapping
        )

        # Since we don't know for sure which one will be, we need to make
        # sure it's one of the items.
        self.assertIn(
            str(wrapper),
            (
                self.mapping['country']['name'],
                self.mapping['country']['province']['name'],
                self.mapping['country']['province']['city']['name'],
            )
        )

    def test_dict_to_obj(self):
        """Test `dict_to_obj`.

        :return:
        """
        wrapper = dict_to_obj(self.mapping)
        mapping = obj_to_dict(wrapper)
        self.assertEqual(self.mapping, mapping)

    def test_wrapper_as_json(self):
        """Test :Wrapper:`as_json` property."""
        wrapper = dict_to_obj(self.mapping)
        self.assertEqual(
            json.loads(wrapper.as_json),
            json.loads(
                '{"country": '
                '{"name": "Netherlands", '
                '"province": {'
                '"name": "North Holland", '
                '"city": {'
                '"name": "Amsterdam"}}}}'
            )
        )
