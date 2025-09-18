class FD:

    def __init__(self,price,origin_airport,destination_airport,out_date,return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    def find_cheapest_flight(data):

        if data is None or not data['data']:

            print("No flight data with one stop.")
            return FD("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

        first_flight = data['data'][0]
        lowest_price = float(first_flight["price"]["grandTotal"])
        nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
        origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
        out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

        cheapest_flight = FD(lowest_price, origin, destination, out_date, return_date, nr_stops)

        for flight in data["data"]:

            price = float(flight["price"]["grandTotal"])
            if price < lowest_price:

                lowest_price = price
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

                cheapest_flight = FD(lowest_price, origin, destination, out_date, return_date, nr_stops)

        return cheapest_flight
