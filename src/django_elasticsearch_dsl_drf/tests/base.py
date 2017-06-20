import logging

from django.test import TransactionTestCase
import pytest
from rest_framework.test import APIClient

import factories

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
class BaseTestCase(TransactionTestCase):
    """Generic base class with shared logic for all tests."""

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
