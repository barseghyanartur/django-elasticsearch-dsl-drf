# coding: utf-8
"""
Pagination.
"""

from __future__ import unicode_literals

from collections import OrderedDict

from django.core import paginator as django_paginator

from elasticsearch_dsl.utils import AttrDict

from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

import six

# from .compat import get_count
from .versions import ELASTICSEARCH_GTE_6_0

__title__ = 'django_elasticsearch_dsl_drf.pagination'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'LimitOffsetPagination',
    'Page',
    'PageNumberPagination',
    'Paginator',
)


class Page(django_paginator.Page):
    """Page for Elasticsearch."""

    def __init__(self, object_list, number, paginator, facets):
        self.facets = facets
        if isinstance(object_list.hits.total, AttrDict):
            self.count = object_list.hits.total.value
        else:
            self.count = object_list.hits.total
        super(Page, self).__init__(object_list, number, paginator)


class Paginator(django_paginator.Paginator):
    """Paginator for Elasticsearch."""

    def page(self, number):
        """Returns a Page object for the given 1-based page number.

        :param number:
        :return:
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        object_list = self.object_list[bottom:top].execute()
        __facets = getattr(object_list, 'aggregations', None)
        return self._get_page(object_list, number, self, facets=__facets)

    def _get_page(self, *args, **kwargs):
        """Get page.

        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)


class PageNumberPagination(pagination.PageNumberPagination):
    """Page number pagination.

    A simple page number based style that supports page numbers as
    query parameters.

    Example:

        http://api.example.org/accounts/?page=4
        http://api.example.org/accounts/?page=4&page_size=100
    """

    django_paginator_class = Paginator

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param args:
        :param kwargs:
        """
        self.facets = None
        # self.page = None
        # self.request = None
        self.count = None
        super(PageNumberPagination, self).__init__(*args, **kwargs)

    def get_facets(self, page=None):
        """Get facets.

        :param page:
        :return:
        """
        if page is None:
            page = self.page

        if hasattr(page, 'facets') and hasattr(page.facets, '_d_'):
            return page.facets._d_

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate a queryset.

        Paginate a queryset if required, either returning a page object,
        or `None` if pagination is not configured for this view.

        :param queryset:
        :param request:
        :param view:
        :return:
        """
        # TODO: It seems that paginator breaks things. If take out, queries
        # doo work.
        # Check if there are suggest queries in the queryset,
        # ``execute_suggest`` method shall be called, instead of the
        # ``execute`` method and results shall be returned back immediately.
        # Placing this code at the very start of ``paginate_queryset`` method
        # saves us unnecessary queries.
        is_suggest = getattr(queryset, '_suggest', False)
        if is_suggest:
            if ELASTICSEARCH_GTE_6_0:
                return queryset.execute().to_dict().get('suggest')
            return queryset.execute_suggest().to_dict()

        # Check if we're using paginate queryset from `functional_suggest`
        # backend.
        if view.action == 'functional_suggest':
            return queryset

        # If we got to this point, it means it's not a suggest or functional
        # suggest case.

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        # Something weird is happening here. If None returned before the
        # following code, post_filter works. If None returned after this code
        # post_filter does not work. Obviously, something strange happens in
        # the paginator.page(page_number) and thus affects the lazy
        # queryset in such a way, that we get TransportError(400,
        # 'parsing_exception', 'request does not support [post_filter]')
        try:
            self.page = paginator.page(page_number)
        except django_paginator.InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response_context(self, data):
        """Get paginated response data.

        :param data:
        :return:
        """
        __data = [
            ('count', self.page.count),
            # ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ]
        __facets = self.get_facets()
        if __facets is not None:
            __data.append(
                ('facets', __facets),
            )
        __data.append(
            ('results', data),
        )
        return __data

    def get_paginated_response(self, data):
        """Get paginated response.

        :param data:
        :return:
        """
        return Response(OrderedDict(self.get_paginated_response_context(data)))

    def get_count(self, es_response):
        if isinstance(es_response.hits.total, AttrDict):
            return es_response.hits.total.value
        return es_response.hits.total


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """A limit/offset pagination.

    Example:

        http://api.example.org/accounts/?limit=100
        http://api.example.org/accounts/?offset=400&limit=100
    """

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param args:
        :param kwargs:
        """
        self.facets = None
        self.count = None
        # self.limit = None
        # self.offset = None
        # self.request = None
        super(LimitOffsetPagination, self).__init__(*args, **kwargs)

    def paginate_queryset(self, queryset, request, view=None):
        # Check if there are suggest queries in the queryset,
        # ``execute_suggest`` method shall be called, instead of the
        # ``execute`` method and results shall be returned back immediately.
        # Placing this code at the very start of ``paginate_queryset`` method
        # saves us unnecessary queries.
        is_suggest = getattr(queryset, '_suggest', False)
        if is_suggest:
            if ELASTICSEARCH_GTE_6_0:
                return queryset.execute().to_dict().get('suggest')
            return queryset.execute_suggest().to_dict()

        # Check if we're using paginate queryset from `functional_suggest`
        # backend.
        if view.action == 'functional_suggest':
            return queryset

        # If we got to this point, it means it's not a suggest or functional
        # suggest case.

        # if hasattr(self, 'get_count'):
        #     self.count = self.get_count(queryset)
        # else:
        #     from rest_framework.pagination import _get_count
        #     self.count = _get_count(queryset)

        # self.count = get_count(self, queryset)

        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request

        resp = queryset[self.offset:self.offset + self.limit].execute()
        self.facets = getattr(resp, 'aggregations', None)

        self.count = self.get_count(resp)

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(resp)

    def get_facets(self, facets=None):
        """Get facets.

        :param facets:
        :return:
        """
        if facets is None:
            facets = self.facets

        if facets is None:
            return None

        if hasattr(facets, '_d_'):
            return facets._d_

    def get_paginated_response_context(self, data):
        """Get paginated response data.

        :param data:
        :return:
        """
        __data = [
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ]
        __facets = self.get_facets()
        if __facets is not None:
            __data.append(
                ('facets', __facets),
            )
        __data.append(
            ('results', data),
        )
        return __data

    def get_paginated_response(self, data):
        """Get paginated response.

        :param data:
        :return:
        """
        return Response(OrderedDict(self.get_paginated_response_context(data)))

    def get_count(self, es_response):
        if isinstance(es_response.hits.total, AttrDict):
            return es_response.hits.total.value
        return es_response.hits.total
