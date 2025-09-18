import os
import requests

class FS:

    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()


    def _get_new_token(self):

        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=os.getenv("AMADEUS_TOKEN_ENDPOINT"),data=body,headers=header)
        print(f"The Amadeus access token expires in: {response.json()['expires_in']} seconds")
        return response.json()["access_token"]


    def iataSearch(self, city):
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        body = {
            'keyword':city,
            "subType": "CITY"
        }
        response = requests.get(url="https://test.api.amadeus.com/v1/reference-data/locations",
                                params=body, headers=header)

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct="true"):

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "INR",
            "max": "10",
        }
        response = requests.get(
            url=os.getenv("FLIGHT_ENDPOINT"),
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}.\nThere was a problem with the flight search.")
            print("Response body:", response.text)
            return None

        return response.json()