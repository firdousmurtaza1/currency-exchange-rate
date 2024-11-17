# -*- coding: utf-8 -*-

from decimal import Decimal

from api.models import Currency, CurrencyExchangeRate

from .async_helpers import load_historical_data


def load_historical_data_task(base, date, symbol):
    """
    The task that fetches historical data asynchronously.
    """

    data = load_historical_data(base, date, symbol)

    exchange_rates = data.get("rates", {})

    source_currency, created = Currency.objects.get_or_create(code=base)
    exchange_rate_instances = []

    # Process each exchanged currency rate
    for symbol, rate_value in exchange_rates.items():
        # Get or create the exchanged currency (target currency)
        exchanged_currency, created = Currency.objects.get_or_create(code=symbol)

        exchange_rate_instance = CurrencyExchangeRate(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=date,
            rate_value=Decimal(
                rate_value
            ),  # Ensure that the rate is stored as a Decimal
        )

        exchange_rate_instances.append(exchange_rate_instance)

    CurrencyExchangeRate.objects.bulk_create(exchange_rate_instances)

    return data
