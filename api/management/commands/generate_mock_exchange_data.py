import json
import os
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from decimal import Decimal
import random
from api.models import Currency, CurrencyExchangeRate

class Command(BaseCommand):
    help = 'Generates mock exchange rate data for testing purposes'

    def handle(self, *args, **kwargs):
        # Define the file name (assuming the file is in the same directory as the command)
        json_file = os.path.join(os.path.dirname(__file__), 'data.json')

        try:
            # Read the JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Extract values from the JSON data
            base_currency = data['base_currency']
            start_date_str = data['start_date']
            end_date_str = data['end_date']
            symbols = data['symbols']

            # Parse dates
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid date format. Use YYYY-MM-DD."))
                return

            # Get or create the base currency
            base_currency_obj, created = Currency.objects.get_or_create(code=base_currency)

            # Prepare a list to store the exchange rate instances
            exchange_rate_instances = []

            # Generate mock exchange rates for the given date range
            current_date = start_date
            while current_date <= end_date:
                for symbol in symbols:
                    # Get or create the exchanged currency
                    exchanged_currency, created = Currency.objects.get_or_create(code=symbol)

                    # Generate a random exchange rate within a realistic range (1 to 150 for example)
                    rate_value = Decimal(random.uniform(1.0, 150.0)).quantize(Decimal('0.000001'))

                    # Create a new exchange rate instance
                    exchange_rate_instance = CurrencyExchangeRate(
                        source_currency=base_currency_obj,
                        exchanged_currency=exchanged_currency,
                        valuation_date=current_date,
                        rate_value=rate_value
                    )

                    # Add to the list of instances
                    exchange_rate_instances.append(exchange_rate_instance)

                # Move to the next day
                current_date += timedelta(days=1)

            # Bulk create the exchange rate instances for efficiency
            CurrencyExchangeRate.objects.bulk_create(exchange_rate_instances)

            self.stdout.write(self.style.SUCCESS(f"Successfully generated mock exchange rates from {start_date_str} to {end_date_str}."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File 'data.json' not found in the current directory."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON in file 'data.json'."))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing key in JSON data: {e}."))
