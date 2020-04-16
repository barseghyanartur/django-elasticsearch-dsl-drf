from faker import Faker as OriginalFaker
from factory.base import Factory
from factory import Faker, LazyAttribute

from search_indexes.documents import AnimalDocument

FAKER = OriginalFaker()

__all__ = (
    'AnimalFactory',
)


class AnimalFactory(Factory):
    """Animal factory."""

    class Meta(object):
        model = AnimalDocument

    scope = LazyAttribute(lambda x: {
        'farm_id': FAKER.uuid4(),
        'holding_id': FAKER.uuid4(),
    })
    action = Faker('word')
    entity = 'animal'
    id = Faker('uuid4')
    app = "s4farm-api"
    message_id = Faker('uuid4')
    publish_date = Faker('date')
    data = LazyAttribute(lambda x: {
        'id': FAKER.pyint(),
        'genetic': {
            'id': FAKER.pyint(),
            'name': FAKER.sentence(nb_words=3),
        },
        'animal_type': {
            'id': FAKER.pyint(),
            'name': FAKER.word(),
            'gender': {
                'id': FAKER.pyint(),
                'name': FAKER.random_sample(['Male', 'Female'])[0]
            }
        },
        'uuid': FAKER.uuid4(),
    })
