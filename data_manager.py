import requests
from pprint import pprint
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()


class DataManager:

    def __init__(self):
        self.user = os.getenv("SHEETY_USERNAME")
        self.password = os.getenv("SHEETY_PASSWORD")
        self.prices_endpoint = os.getenv("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.destination_data = []
        self.customer_data = []

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=self.prices_endpoint, auth=self.authorization)
        response.raise_for_status()
        data = response.json()
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        self.destination_data = data["prices"]
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(
                url=f"{self.prices_endpoint}/{city["id"]}",
                auth=self.authorization,
                json=new_data
            )
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self.authorization)
        response.raise_for_status()
        data = response.json()
        # See how Sheet data is formatted so that you use the correct column name!
        # pprint(data)
        # Name of spreadsheet 'tab' with the customer emails should be "users".
        self.customer_data = data["users"]
        return self.customer_data
