# -*- coding: utf-8 -*-

"""
Base ViewSets.
"""
from __future__ import absolute_import, unicode_literals

import copy

from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .pagination import PageNumberPagination
from .utils import DictionaryProxy
from .versions import ELASTICSEARCH_GTE_7_0

__title__ = 'django_elasticsearch_dsl_drf.viewsets'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseDocumentViewSet',
    'DocumentViewSet',
    'FunctionalSuggestMixin',
    'MoreLikeThisMixin',
    'SuggestMixin',
)


class SuggestMixin(object):
    """Suggest mixin."""

    @action(detail=False)
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


class FunctionalSuggestMixin(object):
    """Functional suggest mixin."""

    @action(detail=False)
    def functional_suggest(self, request):
        """Functional suggest functionality.

        :param request:
        :return:
        """
        # TODO: leave the following check or remove?
        if 'view' in request.parser_context:
            view = request.parser_context['view']
            filter_backend_names = [
                __b.__name__
                for __b
                in view.filter_backends
            ]
            if 'FunctionalSuggesterFilterBackend' not in filter_backend_names:
                raise ImproperlyConfigured(
                    "To use functional suggester backend you shall add "
                    "`FunctionalSuggesterFilterBackend` to the "
                    "`filter_backends` of your ViewSet."
                )

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        return Response(page)


class MoreLikeThisMixin(object):
    """More-like-this mixin."""

    @action(detail=True)
    def more_like_this(self, request, pk=None, id=None):
        """More-like-this functionality detail view.

        :param request:
        :return:
        """
        if 'view' in request.parser_context:
            view = request.parser_context['view']
            kwargs = copy.copy(getattr(view, 'more_like_this_options', {}))
            id_ = pk if pk else id

            # Use current queryset
            queryset = self.filter_queryset(self.get_queryset())
            # We do not try to get fields from current serializer. On the
            # Elasticsearch side if no ``fields`` value is given, ``_all`` is
            # used, and although some serializers could contain less fields
            # than available, this seems like the best approach. If you want to
            # fall back to ``_all`` of Elasticsearch, leave it empty.
            fields = kwargs.pop('fields', [])
            # if not fields:
            #     serializer_class = self.get_serializer_class()
            #     fields = serializer_class.Meta.fields[:]
            if fields:
                queryset = queryset.query(
                    MoreLikeThis(
                        fields=fields,
                        like={
                            '_id': "{}".format(id_),
                            '_index': "{}".format(self.index),
                            '_type': "{}".format(self.mapping)
                        },
                        **kwargs
                    )
                ).sort('_score')
            else:
                queryset = queryset.query(
                    MoreLikeThis(
                        like={
                            '_id': "{}".format(id_),
                            '_index': "{}".format(self.index),
                            '_type': "{}".format(self.mapping)
                        },
                        **kwargs
                    )
                ).sort('_score')

            # Standard list-view implementation
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class BaseDocumentViewSet(ReadOnlyModelViewSet):
    """Base document ViewSet."""

    document_uid_field = 'id'
    document = None  # Re-define
    pagination_class = PageNumberPagination
    # permission_classes = (AllowAny,)
    ignore = []

    def __init__(self, *args, **kwargs):
        assert self.document is not None

        self.client = connections.get_connection(
            self.document._get_using()
        )
        self.index = self.document._index._name
        self.mapping = self.document._doc_type.mapping.properties.name
        self.search = Search(
            using=self.client,
            index=self.index,
            doc_type=self.document._doc_type.name
        )
        super(BaseDocumentViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """Get queryset."""
        queryset = self.search.query()
        # Model- and object-permissions of the Django REST framework (
        # at the moment of writing they are ``DjangoModelPermissions``,
        # ``DjangoModelPermissionsOrAnonReadOnly`` and
        # ``DjangoObjectPermissions``) require ``model`` attribute to be
        # present in the queryset. Unfortunately we don't have that here.
        # The following approach seems to fix that (pretty well), since
        # model and object permissions would work out of the box (for the
        # correspondent Django model/object). Alternative ways to solve this
        # issue are: (a) set the ``_ignore_model_permissions`` to True on the
        # ``BaseDocumentViewSet`` or (b) provide alternative permission classes
        # that are almost identical to the above mentioned classes with
        # the only difference that they know how to extract the model from the
        # given queryset. If you think that chosen solution is incorrect,
        # please make an issue or submit a pull request explaining the
        # disadvantages (and ideally - propose  a better solution). Couple of
        # pros for current solution: (1) works out of the box, (2) does not
        # require modifications of current permissions (which would mean we
        # would have to keep up with permission changes of the DRF).
        queryset.model = self.document.Django.model
        return queryset

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
            get_kwargs = {'id': self.kwargs[lookup_url_kwarg]}
            if self.ignore:
                get_kwargs.update({'ignore': self.ignore})
            obj = self.document.get(**get_kwargs)

            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            if not obj and self.ignore:
                raise Http404("No result matches the given query.")
            return DictionaryProxy(obj.to_dict())
        else:
            queryset = queryset.filter(
                'term',
                **{self.document_uid_field: self.kwargs[lookup_url_kwarg]}
            )

            hits = queryset.execute().hits.hits
            count = len(hits)

            if count == 1:
                obj = hits[0]['_source']

                # May raise a permission denied
                self.check_object_permissions(self.request, obj)
                if ELASTICSEARCH_GTE_7_0:
                    dictionary_proxy = DictionaryProxy(obj.to_dict())
                else:
                    dictionary_proxy = DictionaryProxy(obj)

                return dictionary_proxy

            elif count > 1:
                raise Http404(
                    "Multiple results matches the given query. "
                    "Expected a single result."
                )

            raise Http404("No result matches the given query.")


class DocumentViewSet(BaseDocumentViewSet,
                      SuggestMixin,
                      FunctionalSuggestMixin):
    """DocumentViewSet with suggest and functional-suggest mix-ins."""
