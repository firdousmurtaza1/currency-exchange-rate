# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal


class ExchangeRateProvider(ABC):
    @abstractmethod
    def get_exchange_rate(
        self, source_currency, exchanged_currency, valuation_date: date
    ) -> Decimal:
        pass
