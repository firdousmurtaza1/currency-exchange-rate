from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import date

class ExchangeRateProvider(ABC):
    @abstractmethod
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date: date) -> Decimal:
        pass
