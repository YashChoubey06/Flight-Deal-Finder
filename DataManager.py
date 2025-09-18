import os
import requests
from pprint import pprint

class DM:

    def __init__(self):

        self.customer_data = {}

    def update(self,flight_data):

        header = {
            "Authorization":os.getenv("SHEETY_AUTH")
        }

        for i in flight_data:

            row_id = i["id"]
            query = {
                "price":{
                    "iataCode": i["iataCode"]
                }
            }
            response = requests.put(url=f"{os.getenv("SHEETY_PUTROW_PRICES")}/{row_id}",json=query,headers=header)
            print(response.text)

    def get_customer_emails(self):

        sheety_header = {
            "Authorization": os.getenv("SHEETY_AUTH")
        }

        response = requests.get(url=os.getenv("SHEETY_GETROW_USERS"), headers=sheety_header)
        sheet_data = response.json()
        self.customer_data = sheet_data["users"]

        return self.customer_data