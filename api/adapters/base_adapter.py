class BaseAdapter:
    def fetch_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError
