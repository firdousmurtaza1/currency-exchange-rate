import random
from .base_adapter import BaseAdapter

class MockAdapter(BaseAdapter):
    def fetch_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        # return round(random.uniform(0.5, 1.5), 6)
    
        return {
            'source_currency': source_currency,
            'exchanged_currency': exchanged_currency,
            'valuation_date': valuation_date,
            'rate_value': random.uniform(0.5, 1.5)  # Random mock rate
        }
