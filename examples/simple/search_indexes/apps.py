try:
    from django.apps import AppConfig

    class Config(AppConfig):
        """Config."""

        name = 'search_indexes'
        label = 'search_indexes'

    __all__ = ('Config',)

except ImportError:
    pass
