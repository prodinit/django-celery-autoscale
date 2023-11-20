from datetime import timedelta, datetime, timezone

from celery.decorators import periodic_task
from .monitor import monitor_queues
from .scale import scale_up_support_workers, scale_down_support_workers
from .constants import ONE_MINUTE, THREE_MINUTES


@periodic_task(run_every=timedelta(seconds=ONE_MINUTE), options={"queue": "default"})
def periodic_cloudwatch_monitor():
    monitor_queues()


@periodic_task(run_every=timedelta(seconds=ONE_MINUTE), options={"queue": "default"})
def periodic_task_to_scale_up():
    scale_up_support_workers()


@periodic_task(run_every=timedelta(seconds=THREE_MINUTES), options={"queue": "default"})
def periodic_taks_to_scale_down():
    scale_down_support_workers()
