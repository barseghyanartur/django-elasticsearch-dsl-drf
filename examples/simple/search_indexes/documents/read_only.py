from elasticsearch_dsl import Document

__all__ = (
    'ReadOnlyDocument',
)


class ReadOnlyDocument(Document):

    def clear_cache(self, *args, **kwargs):
        return self

    def close(self, *args, **kwargs):
        return None

    def create(self, *args, **kwargs):
        return None

    def delete(self, *args, **kwargs):
        return None

    def delete_alias(self, *args, **kwargs):
        return None

    def flush(self, *args, **kwargs):
        return None

    def forcemerge(self, *args, **kwargs):
        return None

    def put_mapping(self, *args, **kwargs):
        return None

    def put_settings(self, *args, **kwargs):
        return None

    def save(self, *args, ** kwargs):
        return None

    def settings(self, *args, ** kwargs):
        return None

    def shrink(self, *args, ** kwargs):
        return None

    def updateByQuery(self, *args, ** kwargs):
        return None

    def upgrade(self, *args, ** kwargs):
        return None
