from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    AddressDocumentViewSet,
    AuthorDocumentViewSet,
    BookDocumentViewSet,
    BookOrderingByScoreDocumentViewSet,
    BookFunctionalSuggesterDocumentViewSet,
    CityDocumentViewSet,
    PublisherDocumentViewSet,
)

__all__ = ('urlpatterns',)

router = DefaultRouter()

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

books_ordered_by_score = router.register(
    r'books-ordered-by-score',
    BookOrderingByScoreDocumentViewSet,
    base_name='bookdocument_ordered_by_score'
)

books_functional_suggester = router.register(
    r'books-functional-suggester',
    BookFunctionalSuggesterDocumentViewSet,
    base_name='bookdocument_functional_suggester'
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
