import requests
import os
from TBO_hotels.tbo_library.utils import convert_json_to_xml,convert_xml_to_json
import json

class Connection():
    def __init__(self):
        self.url = "http://api.tbotechnology.in/HotelAPI_V7/HotelService.svc"
        self.headers = {'Content-Type': 'application/soap+xml; charset=utf-8'}

    def tbo_xml_wrapper(self,url,body):
        request_body =   '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:hot="http://TekTravel/HotelBookingApi">
                              <soap:Header xmlns:wsa='http://www.w3.org/2005/08/addressing'>
                                <hot:Credentials xmlns:hot="http://TekTravel/HotelBookingApi" UserName="{0}" Password="{1}">
                                </hot:Credentials>
                                <wsa:Action>{2}</wsa:Action>
                                <wsa:To>http://api.tbotechnology.in/hotelapi_v7/hotelservice.svc</wsa:To>
                              </soap:Header>
                              <soap:Body>
                              {3}
                              </soap:Body>
                            </soap:Envelope>'''.format(os.getenv("TBO_Username"), os.getenv("TBO_Password"), url, body)
        return request_body

    def post(self,payload):
        response = requests.request("POST",
                                    url=self.url,
                                    headers=self.headers,
                                    data=payload)

        return convert_xml_to_json(xml_data=response.text)["s:Envelope"]["s:Body"]

    def search_hotel(self,payload):

        body = self.tbo_xml_wrapper(url = "http://TekTravel/HotelBookingApi/HotelSearch",
                                    body= convert_json_to_xml(payload,start_node_name="HotelSearchRequest"))
        response = self.post(payload=body)
        return response["HotelSearchResponse"]["HotelResultList"]["HotelResult"]

    def get_all_counties(self):
        body = self.tbo_xml_wrapper(url="http://TekTravel/HotelBookingApi/CountryList",
                                    body=convert_json_to_xml({}, start_node_name="CountryListRequest xmlns=\"http://TekTravel/HotelBookingApi\""))

        return self.post(payload=body)["CountryListResponse"]["CountryList"]["Country"]

    def get_all_cities_in_county(self,payload):
        body = self.tbo_xml_wrapper(url="http://TekTravel/HotelBookingApi/DestinationCityList",
                                    body=convert_json_to_xml(payload,
                                    start_node_name="DestinationCityListRequest xmlns=\"http://TekTravel/HotelBookingApi\""))

        return self.post(payload=body)["DestinationCityListResponse"]["CityList"]["City"]


