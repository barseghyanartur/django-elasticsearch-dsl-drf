# coding: utf-8
"""
Pagination.
"""

from __future__ import unicode_literals

from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response

__title__ = 'django_elasticsearch_dsl_drf.pagination'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'PageNumberPagination',
)


class PageNumberPagination(pagination.PageNumberPagination):
    """PageNumberPagination."""

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
