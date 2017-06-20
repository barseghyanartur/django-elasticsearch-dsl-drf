from factory import DjangoModelFactory, SubFactory  # , post_generation

from books.models import Order

# from .factory_faker import Faker
# from .books_orderline import OrderLineFactory

__all__ = ('OrderFactory',)


class OrderFactory(DjangoModelFactory):
    """Order factory."""

    owner = SubFactory('factories.auth_user.UserFactory')
    # created = Faker('date')
    # updated = Faker('date')

    class Meta(object):
        """Meta class."""

        model = Order

    # @post_generation
    # def order_lines(obj, created, extracted, **kwargs):
    #     """Create `OrderLine` objects for the created `Order` instance."""
    #     if created:
    #         # Create 4 `OrderLine` objects.
    #         order_lines = OrderLineFactory.create_batch(4, **kwargs)
    #         obj.order_lines.add(*order_lines)
