from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime

from api.forms import CurrencyConverterForm
from api.services.beacon_rate_provider import CurrencyBeaconProvider
from api.services.mock_service_provider import MockExchangeRateProvider
from .services.provider_service import ProviderService, get_exchange_rate_data
from .models import Currency, CurrencyExchangeRate
from .serializers import CurrencyExchangeRateSerializer, CurrencySerializer  # Create this serializer
from rest_framework import generics
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django_q.tasks import async_task

class CurrencyListCreate(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


# Retrieve, update, or delete a specific currency
class CurrencyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyRatesList(APIView):
    """
    API view to retrieve a list of currency exchange rates for a specific time period.
    """

    def get(self, request):
        # Extract query parameters
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Validate required parameters
        if not source_currency or not date_from or not date_to:
            return Response(
                {"error": "source_currency, date_from, and date_to are required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate date format
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch exchange rates from the database if available
        exchange_rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=(date_from, date_to),
        )

        if exchange_rates.exists():
            # Serialize and return data if it exists in the database
            serializer = CurrencyExchangeRateSerializer(exchange_rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If data is not in the database, call ProviderService to fetch from external providers
        provider_service = ProviderService()
        try:
            # Fetch exchange rates for the specified date range
            rate = provider_service.get_exchange_rate_timeseries(
                source_currency, None, date_from, date_to
            )
            if rate:
                return Response(rate, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If no rates are found
        return Response(
            {"error": "No exchange rates found for the given criteria."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
class ConvertAmountView(APIView):
    """
    API view to convert an amount from one currency to another using either a stored rate
    or a live rate from an external provider.
    """

    def get(self, request):
        # Extract query parameters
        from_currency = request.query_params.get('source_currency')
        to_currency = request.query_params.get('exchanged_currency')
        amount = request.query_params.get('amount')

        # Check if all required parameters are provided
        if not all([from_currency, to_currency, amount]):
            return Response(
                {"error": "Missing required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Try fetching the exchange rate from the database
            rate = CurrencyExchangeRate.objects.filter(
                source_currency__code=from_currency,
                exchanged_currency__code=to_currency,
            ).latest('valuation_date').rate_value

            # Calculate the converted amount
            converted_amount = float(amount) * float(rate)

            return Response(
                {"rate": rate, "converted_amount": converted_amount},
                status=status.HTTP_200_OK,
            )
        except CurrencyExchangeRate.DoesNotExist:
            # If rate not found in the database, fetch live rate from the provider
            try:
                provider = ProviderService()  # Ensure ProviderService is implemented correctly
                live_rate = provider.get_conversion_rate(from_currency, to_currency, float(amount))

                # Extract the rate from the live response
                rate = live_rate["response"]["value"]
                converted_amount = float(amount) * rate

                return Response(
                    {"rate": rate, "converted_amount": converted_amount},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to fetch live rate: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )




class ExchangeRateView(APIView):
    """
    API view to fetch the exchange rate between two currencies for a specific valuation date.
    """

    def get(self, request, *args, **kwargs):
        # Get query parameters for currencies, valuation date, and provider
        source_currency_code = request.query_params.get('source_currency')
        exchanged_currency_code = request.query_params.get('exchanged_currency')
        valuation_date_str = request.query_params.get('valuation_date')
        provider_name = request.query_params.get('provider', 'mock')  # Default to Mock provider

        # Validate input parameters
        if not source_currency_code or not exchanged_currency_code or not valuation_date_str:
            return Response(
                {"error": "Missing required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            source_currency = Currency.objects.get(code=source_currency_code)
            exchanged_currency = Currency.objects.get(code=exchanged_currency_code)
            valuation_date = datetime.strptime(valuation_date_str, '%Y-%m-%d').date()
        except Currency.DoesNotExist:
            return Response({"error": "Currency not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(
                {"error": "Invalid valuation date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Choose the provider based on the 'provider' parameter
        if provider_name == 'currencybeacon':
            provider = CurrencyBeaconProvider()  # Replace with your actual API key
        else:
            provider = MockExchangeRateProvider()

        # Call the function to get the exchange rate data
        try:
            rate = get_exchange_rate_data(
                source_currency.code, exchanged_currency.code, valuation_date, provider
            )

            CurrencyExchangeRate.create_from_provider(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date,
                rate_value=rate,
            )

            return Response({"exchange_rate": str(rate)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoricalDataView(View):
    """
    A Django class-based view to initiate loading of historical exchange rate data.
    """

    def get(self, request, *args, **kwargs):
        base = request.GET.get('base', 'USD')  # Default to 'USD' if no base is provided
        date = request.GET.get('date')  # Historical date required
        symbols = request.GET.get('symbols', '').split(',')  # Symbols should be a comma-separated list

        if not date:
            return JsonResponse({'error': 'Date is required.'}, status=400)

        if not symbols:
            return JsonResponse({'error': 'At least one symbol is required.'}, status=400)

        # Trigger the Django Q task to load the historical data asynchronously
        async_task('api.tasks.load_historical_data_task', base, date, symbols)

        return JsonResponse({'message': 'Task started! The data will be processed in the background.'})
    

    

@method_decorator(staff_member_required, name='dispatch')
class CurrencyConverterAdminView(View):
    template_name = "admin/currency_converter.html"

    def get(self, request):
        # Display the form
        form = CurrencyConverterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # Handle form submission
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            source_currency = form.cleaned_data["source_currency"]
            amount = form.cleaned_data["amount"]
            target_currencies = form.cleaned_data["target_currencies"]

            conversion_results = []

            # Get today's date for the latest rates
            today = date.today()

            for target_currency in target_currencies:
                # Fetch the latest exchange rate
                try:
                    exchange_rate = CurrencyExchangeRate.objects.get(
                        source_currency=source_currency,
                        exchanged_currency=target_currency,
                        valuation_date=today
                    )
                    converted_amount = amount * exchange_rate.rate_value
                    conversion_results.append({
                        "target_currency": target_currency.code,
                        "rate_value": exchange_rate.rate_value,
                        "converted_amount": converted_amount
                    })
                except CurrencyExchangeRate.DoesNotExist:
                    conversion_results.append({
                        "target_currency": target_currency.code,
                        "rate_value": "N/A",
                        "converted_amount": "N/A"
                    })

            return render(request, self.template_name, {
                "form": form,
                "results": conversion_results
            })

        return render(request, self.template_name, {"form": form})


