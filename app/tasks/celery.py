from celery import Celery

from app.config import settings as s

celery = Celery(
    'tasks',
    broker=f"redis://{s.REDIS_URL}",
    include=['app.tasks.tasks'],
    broker_connection_retry_on_startup=True
)