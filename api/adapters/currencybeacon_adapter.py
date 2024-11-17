# -*- coding: utf-8 -*-
import requests

from api.models import Currency
from core import settings

from .base_adapter import BaseAdapter


class CurrencyBeaconAdapter(BaseAdapter):
    # API_URL = "https://api.currencybeacon.com/v1/latest"
    # BASE_URL = "https://api.currencybeacon.com/v1"
    # API_KEY = "wJfoVxcwYQII319HNEiLDawHnZuPsCpM"

    def fetch_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        url = f"{settings.API_BASE_URL}/latest"
        response = requests.get(
            url,
            params={
                "api_key": settings.API_KEY,
                "base": source_currency,
                "symbols": exchanged_currency,
            },
        )
        data = response.json()
        return data.get("rates", {}).get(exchanged_currency)

    def fetch_exchange_rate_timeseries(
        self, source_currency, exchanged_currency, date_from, date_to
    ):
        """Fetches exchange rates for a range of dates (timeseries)."""
        url = f"{settings.API_BASE_URL}/timeseries"

        params = {
            "api_key": settings.API_KEY,
            "base": source_currency,
            "symbols": ",".join(Currency.objects.values_list("code", flat=True)),
            "start_date": date_from.strftime("%Y-%m-%d"),
            "end_date": date_to.strftime("%Y-%m-%d"),
        }
        response = requests.get(url, params=params)

        return response.json() if response.status_code == 200 else None

    def fetch_conversion_rate(self, source_currency, exchanged_currency, amount):
        """Fetches the conversion rate for a specific amount."""
        url = f"{settings.API_BASE_URL}/convert"
        params = {
            "api_key": settings.API_KEY,
            "from": source_currency,
            "to": exchanged_currency,
            "amount": amount,
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
