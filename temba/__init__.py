__version__ = "8.3.102"

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .temba_celery import app as celery_app  # noqa
