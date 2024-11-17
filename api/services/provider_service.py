# -*- coding: utf-8 -*-
from decimal import Decimal

from api.services.exchange_rate_provider import ExchangeRateProvider

from ..adapters.currencybeacon_adapter import CurrencyBeaconAdapter
from ..adapters.mock_adapter import MockAdapter
from ..models import Provider  # Adjust import if Provider model is in a different app


class ProviderService:
    PROVIDERS = {
        "CurrencyBeacon": CurrencyBeaconAdapter(),
        "Mock": MockAdapter(),
    }

    def get_exchange_rate_data(
        source_currency, exchanged_currency, valuation_date
    ) -> Decimal:
        Provider.objects.filter(is_active=True).order_by("priority")
        providers = Provider.objects.filter(is_active=True).order_by("priority")

        for provider in providers:
            try:
                # Assuming that each provider has a method `get_exchange_rate` which accepts the relevant parameters.
                exchange_rate = provider.get_exchange_rate(
                    source_currency, exchanged_currency, valuation_date
                )

                # If the provider returns a valid rate, return it
                if exchange_rate is not None:
                    return Decimal(exchange_rate)

            except Exception as e:
                # If there is an exception (provider failure), move to the next provider

                continue

        # If no provider was successful, raise an exception or return a default error rate
        raise Exception("All providers failed to retrieve the exchange rate.")

    def get_exchange_rate(
        self, source_currency, exchanged_currency, valuation_date, provider
    ):
        for provider in Provider.objects.filter(is_active=True).order_by("priority"):

            try:
                adapter = self.PROVIDERS[provider.name]

                rate = adapter.fetch_exchange_rate(
                    source_currency, exchanged_currency, valuation_date
                )

                if rate:
                    return rate
            except Exception as e:
                # Log provider failure (e.g., logging.error(f"Provider {provider.name} failed: {e}"))
                continue
        raise ValueError("No provider could fetch the data.")

    def get_exchange_rate_timeseries(
        self, source_currency, exchanged_currency, date_from, date_to
    ):
        """Range retrieval with fallback to multiple providers"""

        for provider in Provider.objects.filter(is_active=True).order_by("priority"):

            adapter = self.PROVIDERS[provider.name]

            try:
                rates_data = adapter.fetch_exchange_rate_timeseries(
                    source_currency, exchanged_currency, date_from, date_to
                )

                if rates_data:
                    return rates_data
            except Exception:
                continue
        raise ValueError("No provider could fetch data for the specified range.")

    def get_conversion_rate(self, source_currency, exchanged_currency, amount):
        """Direct conversion rate retrieval"""
        for provider in Provider.objects.filter(is_active=True).order_by("priority"):
            adapter = self.PROVIDERS[provider.name]
            try:
                rate_data = adapter.fetch_conversion_rate(
                    source_currency, exchanged_currency, amount
                )
                if rate_data:
                    return rate_data
            except Exception:
                continue
        raise ValueError("No provider could fetch conversion data.")


def get_exchange_rate_data(
    source_currency, exchanged_currency, valuation_date, provider: ExchangeRateProvider
) -> Decimal:
    return provider.get_exchange_rate(
        source_currency, exchanged_currency, valuation_date
    )
