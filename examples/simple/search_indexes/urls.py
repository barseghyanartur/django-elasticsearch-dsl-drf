from django.conf.urls import url, include
from .rest_framework_extensions_routers_compat import ExtendedDefaultRouter
# from rest_framework_extensions.routers import ExtendedDefaultRouter
from .viewsets import (
    AddressDocumentViewSet,
    AuthorDocumentViewSet,
    BookDocumentViewSet,
    CityDocumentViewSet,
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

cities = router.register(
    r'cities',
    CityDocumentViewSet,
    base_name='citydocument'
)

publishers = router.register(
    r'publishers',
    PublisherDocumentViewSet,
    base_name='publisherdocument'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
