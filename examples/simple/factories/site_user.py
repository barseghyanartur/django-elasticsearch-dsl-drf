from factory import Faker
from factory.base import Factory

from search_indexes.documents import SiteUser


__all__ = (
    'SiteUserFactory',
)


class SiteUserFactory(Factory):
    """User factory."""

    class Meta(object):
        model = SiteUser

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    created_at = Faker('date')
    email = Faker('email')
    is_active = Faker('pybool')
