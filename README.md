# Django celery autoscale

Django application to scale celery workers based on number of tasks in redis queues.


## Intro

The message queues have variable amount of load and needs a auto scaling solution, the default and common metrics you have is CPU utilisation and memory utilisation. Unfortunately these metrics are not the best auto scaling solution in case of variable load.

This django package scales the workers based on the load in queues, instead of running bigger instances and save cost as well.



### How to do?
It's quite simple to use. Install with:
```pip install git+https://github.com/prodinit/django-celery-autoscale.git@main```

Next step is to  add `celery_autoscale` to your INSTALLED_APPS like so:

```
INSTALLED_APPS = [
    #... apps I don't care about here
    'celery_autoscale',
]
```

Next step is to add `CELERY_QUEUES` and `CELERY_BROKER_URL` in your django settings.
```
from kombu import Queue

CELERY_QUEUES = (
    Queue('default'),
    Queue('queue1'),
    Queue('queue2'),
)
CELERY_BROKER_URL = ""
```

Next step is to add a few AWS config variables in your django settings.
```
CLUSTER_NAME = ''
SERVICE_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_DEFAULT_REGION = ''
```

## Dependencies
- Python
- Django
- Redis
- Boto3
- AWS ECS
- Celery

## How to customize it?

Well, fork it, clone it, make necessary changes as per your application architecture, use it.

## Bugs?
Raise an issue, I'll check it out.

## Contributions?
Oh well... Make a PR