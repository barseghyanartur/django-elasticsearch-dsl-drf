try:
    from django.apps import AppConfig

    class Config(AppConfig):
        """Config."""

        name = 'books'
        label = 'books'

    __all__ = ('Config',)

except ImportError:
    pass
