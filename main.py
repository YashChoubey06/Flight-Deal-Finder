import requests
import os
from FlightSearch import FS
from DataManager import DM
from pprint import pprint
from dotenv import load_dotenv
from datetime import datetime,timedelta
import time
from FlightData import FD
from twilio.rest import Client
from NotifManager import NM


load_dotenv()
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

origin_city_iata = "LON"
flight_search = FS()
notif_sender = NM()
data_manager = DM()

sheety_putrow = os.getenv("SHEETY_PUTROW_PRICES")
sheety_getrow = os.getenv("SHEETY_GETROW_PRICES")
sheety_addrow = os.getenv("SHEETY_ADDROW_PRICES")

sheety_header ={
    "Authorization":os.getenv("SHEETY_AUTH")
}

response = requests.get(url=sheety_getrow, headers=sheety_header)
sheet_data = response.json()["prices"]

#For updating iata codes in countries, only to be ran first time after filling city names
#
# for i in sheet_data:
#     city_name = i["city"].upper()
#     i["iataCode"] = fs.iataSearch(city_name)
#
# dm = DM()
# dm.update(sheet_data)


for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        origin_city_code=origin_city_iata,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = FD.find_cheapest_flight(flights)
    print(f"{destination['city']}: ₹ {cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price == "N/A":

        print("Checking again for non-direct flights...")
        flights = flight_search.check_flights(
            origin_city_code=origin_city_iata,
            destination_city_code=destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct = "false"
        )

        cheapest_flight = FD.find_cheapest_flight(flights)
        print(f"{destination['city']}: ₹{cheapest_flight.price}")
        time.sleep(2)

    elif cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}.")

        message_body = f"Low price alert! Only INR {cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, on {cheapest_flight.out_date} until {cheapest_flight.return_date}."

        notif_sender.send_sms(
            message_body=message_body
        )

        customer_data = data_manager.get_customer_emails()
        customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
        notif_sender.send_mails(customer_email_list, message_body)