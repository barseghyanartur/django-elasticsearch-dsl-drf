import os

__all__ = (
    'gettext',
    'project_dir',
    'PROJECT_DIR',
)


def project_dir(base):
    """Absolute path to a file from current directory."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), base).replace('\\', '/')
    )


def gettext(val):
    """Dummy gettext."""
    return val


PROJECT_DIR = project_dir
