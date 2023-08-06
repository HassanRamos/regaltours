import os
from django.http import Http404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.openapi import IN_QUERY, IN_PATH, Parameter, TYPE_STRING
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404,render
from .utils import create_celery_schedule,create_periodic_task
from .serializer import *
from celery import current_app
from rest_framework import filters
from TBO_hotels.models import *
from Viator_Tours.models import *
from itertools import chain
from  Viator_Tours.viator_library.connection import Connection as viator_connection
from  TBO_hotels.tbo_library.connection import Connection as tbo_connection
from django.shortcuts import redirect
from django_celery_beat.models import PeriodicTask, IntervalSchedule

viator_instance = viator_connection()
tbo_instance = tbo_connection()



class SearchDestinationAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[Parameter('destination', IN_QUERY, type='text')],
                         tag="website_apis")
    def get(self, request, product):
        destination = request.query_params.get('destination')
        serializer_class = SearchDestinationSerializer

        if product == "hotel":
            queryset = TBO_Country.objects.filter(country_name__icontains=destination)

            if queryset.count() > 5:
                queryset = queryset[:4]
            else:
                queryset_city = TBO_City.objects.filter(city_name__icontains=destination)
                if queryset_city.count() > 5:
                    queryset_city = queryset_city[:4]
                queryset = list(chain(queryset_city, queryset))
        else:
            queryset = Viator_Destinations.objects.filter(destination_name__icontains=destination)



        serializer = serializer_class(queryset, many=True)

        return Response({"data": serializer.data})

    @swagger_auto_schema(request_body=SearchDestinationSerializer,
                         tag="website_apis")
    def post(self, request,product):
        data = request.POST.dict()
        print(data)

        if product == "hotel":
            return redirect("/hotels?destination={}&checkin_date={}&checkout_date={}&no_of_rooms={}&no_of_adults={}".format(data["hotel_destination"],
                                                                                                                                           data["hotel_checkin_date"],
                                                                                                                                           data["hotel_checkout_date"],
                                                                                                                                           data["hotel_rooms_no"],
                                                                                                                                           data["hotel_adults_no"]))

        else:
            destination = Viator_Destinations.objects.get(destination_name=data["data"]["destination"]).destination_id

            response = viator_instance.search_destintion_by_country(destination=int(destination),
                                                                    start_date=data["data"]["checkin_date"],
                                                                    end_date=data["data"]["checkout_date"])

            print(response)



        return Response({"data": response})

class Home(APIView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
         return render(request, "index-search.html" ,context={})

class Index(APIView):
    @swagger_auto_schema(manual_parameters=[Parameter('path',IN_PATH,type='text'),
                                            Parameter('destination',IN_QUERY,type='text',required=False),
                                            Parameter('checkin_date',IN_QUERY,type='text',required=False),
                                            Parameter('checkout_date', IN_QUERY, type='text',required=False),
                                            Parameter('no_of_rooms', IN_QUERY, type='text',required=False),
                                            Parameter('no_of_adults', IN_QUERY, type='text',required=False),
                                            Parameter('no_of_children', IN_QUERY, type='text',required=False)],
                         auto_schema=None)
    def get(self, request,path):
         context = {}
         if path == "flights":
             page = "flight-search.html"

         elif path == "holiday":
             if request.query_params.get('destination'):
                 destination = request.query_params.get('destination')
                 checkin_date = request.query_params.get('checkin_date')
                 checkout_date = request.query_params.get('checkout_date')
                 no_of_adults = request.query_params.get('no_of_adults')
                 no_of_children = request.query_params.get('no_of_children')
                 no_of_rooms = request.query_params.get('no_of_rooms')

                 try:
                     destination = TBO_Country.objects.get(country_name=destination)
                     type = "country"
                 except:
                     destination = TBO_City.objects.get(city_name=destination)
                     type = "city"

                 payload = {"CheckInDate": checkin_date,
                            "CheckOutDate": checkout_date,
                            "IsNearBySearchAllowed": "false",
                            "PreferredCurrencyCode": "USD",
                            "NoOfRooms": no_of_rooms,
                            "GuestNationality": "KE",
                            "RoomGuests": {
                                "RoomGuest AdultCount=\"{}\" ChildCount=\"{}\"".format(no_of_adults,"0"): ""},
                            "ResultCount": "10",
                            "ResponseTime": "5"}

                 if type == "country":
                     payload["CountryName"] = destination.country_name
                 if type == "city":
                     payload["CityName"] = destination.city_name
                     payload["CityId"] = destination.city_code

                 context["hotels"] = tbo_instance.search_hotel(payload=payload)

             page = "holiday-search.html"
         elif path == "hotels":
             if request.query_params.get('destination'):
                 destination = request.query_params.get('destination')
                 checkin_date = request.query_params.get('checkin_date')
                 checkout_date = request.query_params.get('checkout_date')
                 no_of_adults = request.query_params.get('no_of_adults')
                 no_of_children = request.query_params.get('no_of_children')
                 no_of_rooms = request.query_params.get('no_of_rooms')

                 try:
                     destination = TBO_Country.objects.get(country_name=destination)
                     type = "country"
                 except:
                     destination = TBO_City.objects.get(city_name=destination)
                     type = "city"

                 payload = {"CheckInDate": checkin_date,
                            "CheckOutDate": checkout_date,
                            "IsNearBySearchAllowed": "false",
                            "PreferredCurrencyCode": "USD",
                            "NoOfRooms": no_of_rooms,
                            "GuestNationality": "KE",
                            "RoomGuests": {
                                "RoomGuest AdultCount=\"{}\" ChildCount=\"{}\"".format(no_of_adults,"0"): ""},
                            "ResultCount": "10",
                            "ResponseTime": "5"}

                 if type == "country":
                     payload["CountryName"] = destination.country_name
                 if type == "city":
                     payload["CityName"] = destination.city_name
                     payload["CityId"] = destination.city_code

                 context["hotels"] = tbo_instance.search_hotel(payload=payload)

             page = "hotels-search.html"

         else:
             page = "index-search.html"


         return render(request, page ,context=context)

    @swagger_auto_schema(request_body=SearchDestinationSerializer,tag="website_apis")
    def post(self, request):
        form_data = request.data.dict()

        del form_data["csrfmiddlewaretoken"]

        return Response({"status": "connection_test_status"})

class Background_tasks(APIView):
    @swagger_auto_schema(request_body=BackgroundTasksSerializer,
                         tag="website_apis")
    def post(self, request):
        data = request.data

        schedule, created = IntervalSchedule.objects.get_or_create(every=3600,
                                                                   period=IntervalSchedule.SECONDS, )
        PeriodicTask.objects.create(interval=schedule,  # we created this above.
                                    name='sync {} data'.format(data["task_name"]),
                                    task=data["task_name"])

        return Response({"status": "task {} sucessfully created".format(data["task_name"])})


