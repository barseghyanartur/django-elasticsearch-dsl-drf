# -*- coding: utf-8 -*-

"""
Base ViewSets.
"""
from __future__ import absolute_import, unicode_literals

from django.http import Http404

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from .pagination import PageNumberPagination
from .utils import DictionaryProxy


__title__ = 'django_elasticsearch_dsl_drf.viewsets'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseDocumentViewSet',)


class BaseDocumentViewSet(ReadOnlyModelViewSet):
    """Base document ViewSet."""

    document_uid_field = 'id'
    document = None  # Re-define
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        assert self.document is not None

        self.client = connections.get_connection()
        self.index = self.document._doc_type.index
        self.mapping = self.document._doc_type.mapping.properties.name
        self.search = Search(using=self.client, index=self.index)
        super(BaseDocumentViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """Get queryset."""
        return self.search.query()

    def get_object(self):
        """Get object."""
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in self.kwargs:
            raise AttributeError(
                "Expected view %s to be called with a URL keyword argument "
                "named '%s'. Fix your URL conf, or set the `.lookup_field` "
                "attribute on the view correctly." % (
                    self.__class__.__name__,
                    lookup_url_kwarg
                )
            )

        if lookup_url_kwarg == 'id':
            obj = self.document.get(id=self.kwargs[lookup_url_kwarg])
            return DictionaryProxy(obj.to_dict())
        else:
            queryset = queryset.filter(
                'term',
                **{self.document_uid_field: self.kwargs[lookup_url_kwarg]}
            )

            count = queryset.count()
            if count == 1:
                obj = queryset.execute().hits.hits[0]['_source']
                return DictionaryProxy(obj)

            elif count > 1:
                raise Http404(
                    "Multiple results matches the given query. "
                    "Expected a single result."
                )

            raise Http404("No result matches the given query.")

    @list_route()
    def suggest(self, request):
        """Suggest functionality."""
        queryset = self.filter_queryset(self.get_queryset())
        is_suggest = getattr(queryset, '_suggest', False)
        if not is_suggest:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        page = self.paginate_queryset(queryset)
        return Response(page)
