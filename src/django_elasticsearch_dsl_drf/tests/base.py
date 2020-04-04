"""
Base tests.
"""

from time import sleep
import logging

from django.test import TransactionTestCase
import pytest
from rest_framework.test import APIClient

import factories

from ..pip_helpers import get_installed_packages

__title__ = 'django_elasticsearch_dsl_drf.tests.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseRestFrameworkTestCase',
    'BaseTestCase',
    'CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED',
    'CORE_API_AND_CORE_SCHEMA_MISSING_MSG',
    'CORE_API_IS_INSTALLED',
    'CORE_SCHEMA_IS_INSTALLED',
    'INSTALLED_PACKAGES',
    'SleepMixin',
)

LOGGER = logging.getLogger(__name__)
INSTALLED_PACKAGES = get_installed_packages()
CORE_API_IS_INSTALLED = 'coreapi' in INSTALLED_PACKAGES
CORE_SCHEMA_IS_INSTALLED = 'coreschema' in INSTALLED_PACKAGES
CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED = (
    CORE_API_IS_INSTALLED and CORE_SCHEMA_IS_INSTALLED
)
CORE_API_AND_CORE_SCHEMA_MISSING_MSG = "Skipped because coreapi or " \
                                       "coreschema are not installed!"


WAIT_FOR_INDEX = 2


class SleepMixin(object):
    """Sleep mix-in."""

    @classmethod
    def sleep(cls, wait_for_index=WAIT_FOR_INDEX):
        """Sleep for N seconds.

        :param wait_for_index:
        :return:
        """
        sleep(wait_for_index)


@pytest.mark.django_db
class BaseRestFrameworkTestCase(TransactionTestCase, SleepMixin):
    """Base REST framework test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""

        cls.client = APIClient()

        # Create test user.
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
class BaseTestCase(TransactionTestCase, SleepMixin):
    """Base test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""

        cls.client = APIClient()

        # Create test user.
        cls.user = factories.TestUsernameSuperAdminUserFactory()
