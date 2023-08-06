import json
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule
from datetime import datetime, timedelta


def create_periodic_task(task_name,schedule_instance, task_path, kwargs):
    """
    create a celery periodic task
    """
    task = PeriodicTask.objects.create(
        interval=schedule_instance,
        name=task_name,
        task=task_path,
        args=json.dumps(list(kwargs.values())),
    )
    return task


def create_celery_schedule(time_in_seconds):
    """
    Get or create a celery schedule
    """
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=int(time_in_seconds),
        period=IntervalSchedule.SECONDS,
    )
    return schedule