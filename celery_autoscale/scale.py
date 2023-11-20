import math
import boto3
import logging

from .models import ScalingConfigSetting
from .monitor import _get_queue_names, get_tasks_from_queue
from .aws import get_boto_client

from django.conf import settings

logger = logging.getLogger(__name__)


def scale_down_support_workers():
    """
    A function to monitor the scale down celery worker functionality
    """
    scaling_config: ScalingConfigSetting = ScalingConfigSetting.get_latest_object()
    queues: list = _get_queue_names()
    total_tasks = 0
    for queue in queues:
        task_count: int = get_tasks_from_queue(queue)
        total_tasks += task_count

    if total_tasks == 0 or total_tasks <= scaling_config.scale_down_threshold:
        remove_task_from_service(min_tasks=scaling_config.min_support_workers)


def scale_up_support_workers():
    """
    A function to monitor the scale up celery worker functionality
    """
    scaling_config: ScalingConfigSetting = ScalingConfigSetting.get_latest_object()
    queues: list = _get_queue_names()
    for queue in queues:
        task_count: int = get_tasks_from_queue(queue)
        if task_count >= scaling_config.scale_up_threshold:
            ecs_tasks_to_add: int = math.ceil(
                task_count / scaling_config.consumption_rate
            )
            add_task_to_service(
                ecs_tasks_to_add=ecs_tasks_to_add,
                max_tasks=scaling_config.max_support_workers,
            )


def remove_task_from_service(min_tasks: int):
    """
    This function decreases the desired count to ecs services, resulting in scale down of task definitions
    """
    cluster_name = settings.CLUSTER_NAME
    service_name = settings.SERVICE_NAME
    ecs_client = get_boto_client(
        "ecs",
        settings.AWS_DEFAULT_REGION,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        logger.info(f"Scale down triggered, Updating desired count to {min_tasks}")
        update_worker_service(
            ecs_client, cluster_name, service_name, desired_count=min_tasks
        )
    except Exception as err:
        logger.info(f"Exception occured: {err}")


def add_task_to_service(ecs_tasks_to_add: int, max_tasks: int):
    """
    This function increases the desired count to ecs services, resulting in scale up of task definitions
    """
    cluster_name = settings.CLUSTER_NAME
    service_name = settings.SERVICE_NAME
    ecs_client = get_boto_client(
        "ecs",
        settings.AWS_DEFAULT_REGION,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        service_type = ecs_client.describe_services(
            cluster=cluster_name,
            services=[
                service_name,
            ],
        )["services"][0]
        running_count = service_type["runningCount"]
        pending_count = service_type["pendingCount"]
        total_tasks = running_count + pending_count
        desired_count = running_count + ecs_tasks_to_add
        if desired_count > max_tasks:
            desired_count = max_tasks
        if total_tasks < desired_count:
            logger.info(
                f"Scale up triggered, Updating desired count to {desired_count}"
            )
            update_worker_service(
                ecs_client=ecs_client,
                cluster_name=cluster_name,
                service_name=service_name,
                desired_count=desired_count,
            )
    except Exception as err:
        logger.info(f"Exception occured: {err}")


def update_worker_service(
    ecs_client, cluster_name: str, service_name: str, desired_count: int
):
    try:
        service_type = ecs_client.describe_services(
            cluster=cluster_name,
            services=[
                service_name,
            ],
        )
        if (
            service_type["services"]
            and not service_type["services"][0]["desiredCount"] == desired_count
        ):
            response = ecs_client.update_service(
                cluster=cluster_name, service=service_name, desiredCount=desired_count
            )
            return response["service"]["desiredCount"] == desired_count
    except Exception as err:
        logger.info(f"Exception occured: {err}")
        return False
    else:
        return False
