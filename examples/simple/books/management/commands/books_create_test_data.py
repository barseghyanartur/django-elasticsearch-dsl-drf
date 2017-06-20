from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

import factories


DEFAULT_NUMBER_OF_ITEMS_TO_CREATE = 100


class Command(BaseCommand):
    """Create test data."""

    help = "Create test books data."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            type=int,
                            default=DEFAULT_NUMBER_OF_ITEMS_TO_CREATE,
                            help="Number of items to create.")

    def handle(self, *args, **options):
        if options.get('number'):
            number = options['number']
        else:
            number = DEFAULT_NUMBER_OF_ITEMS_TO_CREATE

        try:
            books = factories.BookFactory.create_batch(number)
            print("{} book objects created.".format(number))
        except Exception as err:
            raise CommandError(str(err))

        try:
            book = factories.SingleBookFactory()
            print("A single book object is created.")
        except Exception as err:
            raise CommandError(str(err))
