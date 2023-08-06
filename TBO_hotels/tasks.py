from __future__ import absolute_import
from celery import shared_task
from .models import *
from datetime import datetime
from TBO_hotels.tbo_library.connection import Connection

Task_max_time_limit = 60*60*24
TBO = Connection()


@shared_task(name="sync_tbo_data",
             time_limit=Task_max_time_limit,
             options={'ignore_result': True, 'expires': 60})
def sync_tbo_data():
    available_countries = TBO.get_all_counties()
    for country in available_countries:
        TBO_Country.objects.get_or_create(country_name=country["@CountryName"],
                                                defaults={"country_code":country["@CountryCode"]})
        available_cities = TBO.get_all_cities_in_county({"CountryCode":country["@CountryCode"]})

        country_instance = TBO_Country.objects.get(country_name=country["@CountryName"])

        for city in available_cities:
            TBO_City.objects.get_or_create(city_name=city["@CityName"],
                                           defaults={"city_code":city["@CityCode"],
                                                     "country":country_instance})

