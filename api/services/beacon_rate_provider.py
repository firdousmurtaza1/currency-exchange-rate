from datetime import date
from decimal import Decimal
import requests

from core import settings

from .exchange_rate_provider import ExchangeRateProvider

class CurrencyBeaconProvider(ExchangeRateProvider):
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = f"{settings.API_BASE_URL}/latest"

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date: date) -> Decimal:
        # Construct the API request URL using the source and exchanged currencies
       
        url = f"{self.base_url}?api_key={self.api_key}&base={source_currency}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()['response']['rates'][exchanged_currency]
   
        
        return Decimal(data)  # Assuming the API response contains a 'rate' field
