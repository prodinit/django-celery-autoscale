import redis
from kombu import Queue

from django.conf import settings

redis_client = redis.from_url(settings.CELERY_BROKER_URL)


def _get_queue_names(queue_tuple: tuple) -> list:
    """
    Get a list of all the queues available
    """
    queues = []
    if queue_tuple and isinstance(queue_tuple[0], Queue):
        queues = [queue.name for queue in queue_tuple]
    return queues


def get_tasks_from_queue(queue: str) -> int:
    """Returns the tasks present in a particular queue"""
    count = 0
    if redis_client.type(queue).decode("utf-8") == "list":
        count = redis_client.llen(queue)
    return count


def monitor_queues():
    # publish cloudwatch metric if required
    pass
