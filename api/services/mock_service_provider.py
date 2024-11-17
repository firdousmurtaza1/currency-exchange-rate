from datetime import date
import random
from decimal import Decimal
from .exchange_rate_provider import ExchangeRateProvider

class MockExchangeRateProvider(ExchangeRateProvider):
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date: date) -> Decimal:
        # Generate a random exchange rate between 0.5 and 1.5
        mock_rate = random.uniform(0.5, 1.5)
        return Decimal(round(mock_rate, 6))
