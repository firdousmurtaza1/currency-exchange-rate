# -*- coding: utf-8 -*-
import asyncio

import aiohttp

from core import settings


async def fetch_historical_data(base, date, symbols):
    """
    Asynchronously fetch historical exchange rate data from the CurrencyBeacon API.
    """
    url = f"{settings.API_BASE_URL}/historical"
    params = {
        "api_key": settings.API_KEY,
        "base": base,
        "date": date,
        "symbols": ",".join(
            symbols
        ),  # Join the list of symbols into a comma-separated string
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
