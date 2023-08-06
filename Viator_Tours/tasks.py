from __future__ import absolute_import
from celery import shared_task
from .models import *
from Viator_Tours.viator_library.connection import Connection

Task_max_time_limit = 60*60*24
VIATOR = Connection()


@shared_task(name="sync_viator_data",
             time_limit=Task_max_time_limit,
             options={'ignore_result': True, 'expires': 60})
def sync_viator_data():
    available_destinations = VIATOR.get_all_destinations()
    for destination in available_destinations:
        Viator_Destinations.objects.get_or_create(destination_name=destination["destinationName"],
                                                  defaults={"destination_id":destination["destinationId"],
                                                            "destination_type":destination["destinationType"]})


