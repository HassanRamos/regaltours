from requests import request
import json
from datetime import datetime
import os

class Connection():
    def __init__(self):
        self.base_url = "https://api.viator.com/partner/"
        self.headers = { 'Accept-Language': 'en-US',
                         'exp-api-key': os.getenv("VIATOR_APIKEY"),
                         'Content-Type': 'application/json',
                         'Accept': 'application/json;version=2.0',

                         }
    def get(self,path):
        response = request("GET",
                           url= self.base_url + path,
                           headers=self.headers)
        return response

    def post(self,path,payload):
        response = request("POST",
                           url=self.base_url + path,
                           headers=self.headers,
                           data=json.dumps(payload))
        return response

    def get_all_destinations(self):
        response = self.get(path="v1/taxonomy/destinations").json()
        return response["data"]

    def get_all_attractions(self,destination):
        payload = { "destId": destination,
                    "topX": "1-3",
                    "sortOrder": "SEO_PUBLISHED_DATE_D"  }
        response = self.post(path="v1/taxonomy/attractions",payload=payload).json()
        return response["data"]


    def search_destintion_by_country(self,destination,flags=[],start_date=None,end_date=None):
        payload = {
            "filtering": {
                "destination": destination,
                "flags": flags,
            },
            "pagination": {
                "start": 1,
                "count": 50
            },
            "currency": "USD"
        }
        if start_date == None:
            payload["filtering"]["startDate"] = datetime.now().now.strftime("%Y-%m-%d")
        else:
            payload["filtering"]["startDate"] = start_date
        if end_date != None:
            payload["filtering"]["endDate"] = end_date

        response = self.post(path="products/search",payload=payload).json()
        print(response)

        return response["products"]





