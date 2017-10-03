from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .viewsets import (
    AddressDocumentViewSet,
    AuthorDocumentViewSet,
    BookDocumentViewSet,
    PublisherDocumentViewSet,
)

__all__ = ('urlpatterns',)

router = ExtendedDefaultRouter()

addresses = router.register(
    r'addresses',
    AddressDocumentViewSet,
    base_name='addressdocument'
)

authors = router.register(
    r'authors',
    AuthorDocumentViewSet,
    base_name='authordocument'
)

books = router.register(
    r'books',
    BookDocumentViewSet,
    base_name='bookdocument'
)

publishers = router.register(
    r'publishers',
    PublisherDocumentViewSet,
    base_name='publisherdocument'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
