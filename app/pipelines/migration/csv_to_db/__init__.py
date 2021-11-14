from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('csv_to_db_migration', broker='redis://localhost:6379/0', backend='redis://localhost:6379')

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

app.conf.update(
    result_expires=3600,
    worker_hijack_root_logger=False,
    worker_redirect_stdouts=False,
    worker_log_color=False,
    task_serializer='json',
    result_serializer='json',
)