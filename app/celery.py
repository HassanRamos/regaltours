from __future__ import absolute_import
from celery import Celery
import os
from dotenv import load_dotenv

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
load_dotenv(env_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE","app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings",namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("REQUEST {0!r}".format(self.request))