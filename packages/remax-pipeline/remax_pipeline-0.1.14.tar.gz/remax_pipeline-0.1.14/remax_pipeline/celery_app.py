from celery import Celery

from .tasks.etl_worker import start_worker

celery_app = Celery("app", broker="pyamqp://myuser:mypassword@localhost:5672//")


@celery_app.task
def run_etl_worker(pages: list):
    start_worker(pages)
