from . import _version

__version__ = _version.get_versions()["version"]

from .celery_app import celery_app
