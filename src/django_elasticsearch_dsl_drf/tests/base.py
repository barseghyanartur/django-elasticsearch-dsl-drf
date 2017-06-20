import logging

from django.test import TransactionTestCase
import pytest
from rest_framework.test import APIClient

import factories

__title__ = 'django_elasticsearch_dsl_drf.tests.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseRestFrameworkTestCase',
    'BaseTestCase',
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
class BaseRestFrameworkTestCase(TransactionTestCase):
    """Base REST framework test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""

        cls.client = APIClient()

        # Create genre coordinator.
        cls.user = factories.TestUsernameSuperAdminUserFactory()

    def authenticate(self):
        """Helper for logging in Genre Coordinator user.

        :return:
        """
        self.client.login(
            username=factories.auth_user.TEST_USERNAME,
            password=factories.auth_user.TEST_PASSWORD
        )


@pytest.mark.django_db
class BaseTestCase(TransactionTestCase):
    """Base test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""

        cls.client = APIClient()

        # Create genre coordinator.
        cls.user = factories.TestUsernameSuperAdminUserFactory()
