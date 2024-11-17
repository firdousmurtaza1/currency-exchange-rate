
from decimal import Decimal
from django_q.tasks import async_task

from api.models import Currency, CurrencyExchangeRate
from .async_helpers import load_historical_data

def load_historical_data_task(base, date, symbol):
    """
    The task that fetches historical data asynchronously.
    """
    # Call the asynchronous helper function to fetch data
    data = load_historical_data(base, date, symbol)
   
    # You can process the data or save it to the database here
    exchange_rates = data.get('rates', {})  # The 'rates' dictionary will contain the exchange rate data
  

    # Get or create the base currency (source currency)
    source_currency, created = Currency.objects.get_or_create(code=base)
    
    # Prepare a list to store the exchange rate instances to bulk insert
    exchange_rate_instances = []

    # Process each exchanged currency rate
    for symbol, rate_value in exchange_rates.items():
        # Get or create the exchanged currency (target currency)
        exchanged_currency, created = Currency.objects.get_or_create(code=symbol)
  
        
        # Create a new CurrencyExchangeRate instance
        exchange_rate_instance = CurrencyExchangeRate(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=date,
            rate_value=Decimal(rate_value)  # Ensure that the rate is stored as a Decimal
        )
        
        # Add the instance to the list
        exchange_rate_instances.append(exchange_rate_instance)
  

    # Bulk create the exchange rate instances
    CurrencyExchangeRate.objects.bulk_create(exchange_rate_instances)

    return data
