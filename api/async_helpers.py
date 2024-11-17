import aiohttp
import asyncio

async def fetch_historical_data(base, date, symbols):
    """
    Asynchronously fetch historical exchange rate data from the CurrencyBeacon API.
    """
    url = 'https://api.currencybeacon.com/v1/historical'
    api_key= "wJfoVxcwYQII319HNEiLDawHnZuPsCpM"
    params = {
        'api_key': api_key,
        'base': base,
        'date': date,
        'symbols': ','.join(symbols),  # Join the list of symbols into a comma-separated string
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            return await response.json()  # Return JSON data from the response

def load_historical_data(base, date, symbols):
    """
    Load historical data asynchronously using aiohttp.
    """
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_historical_data(base, date, symbols))
