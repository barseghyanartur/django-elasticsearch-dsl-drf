import random
import factory
from factory import Faker, LazyAttribute
from factory.base import Factory
from factory.fuzzy import FuzzyChoice

from search_indexes.documents import PostDocument


__all__ = (
    'Comment',
    'CommentFactory',
    'PostFactory',
    'ManyViewsPostFactory',
)


class Serializable(object):

    def items(self):
        return self.to_dict().items()

    def to_dict(self):
        return self.__dict__


class Comment(Serializable):
    """Comment model (we need one for factories)."""

    def __init__(self, *args, **kwargs):
        self.author = kwargs.get('author')
        self.content = kwargs.get('content')
        self.created_at = kwargs.get('created_at')


class Tag(Serializable):
    """Tag model (we need one for factories)."""

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')


class CommentFactory(Factory):
    """Comment factory."""

    author = Faker('name')
    content = Faker('text')
    created_at = Faker('date')

    class Meta(object):
        model = Comment


TAGS = (
    'article',
    'package',
    'models',
    'black and white',
    'programming',
    'photography',
    'art',
)


class PostFactory(Factory):
    """Post factory."""

    class Meta(object):
        model = PostDocument

    title = Faker('text', max_nb_chars=10)
    content = Faker('text')
    created_at = Faker('date')
    published = FuzzyChoice([True, False])
    category = FuzzyChoice([
        'Elastic',
        'MongoDB',
        'Machine Learning',
        'Model Photography',
        'Python',
        'Django',
    ])
    num_views = Faker('pyint', min_value=0, max_value=1000)
    tags = LazyAttribute(lambda x: random.sample(TAGS, 4))

    @factory.post_generation
    def comments(obj, create, extracted, **kwargs):
        if create:
            obj.comments = CommentFactory.create_batch(
                size=random.randint(1, 6)
            )


class ManyViewsPostFactory(PostFactory):
    num_views = Faker('pyint', min_value=2000, max_value=10000)
