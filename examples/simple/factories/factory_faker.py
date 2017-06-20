# coding=utf-8

from __future__ import unicode_literals

from factory import Faker as OriginalFaker

__all__ = ('Faker',)


class Faker(OriginalFaker):
    """Override to change the default locale."""

    _DEFAULT_LOCALE = 'nl_NL'
