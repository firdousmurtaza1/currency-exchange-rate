
from django.urls import path
from .views import CurrencyListCreate, CurrencyRatesList, CurrencyRetrieveUpdateDestroy, ConvertAmountView, ExchangeRateView, HistoricalDataView

urlpatterns = [
    path('exchange-rate/', ExchangeRateView.as_view(), name='exchange-rate'),
    path('currencies/', CurrencyListCreate.as_view(), name='currency-list-create'),
    path('currencies/<int:pk>/', CurrencyRetrieveUpdateDestroy.as_view(), name='currency-retrieve-update-destroy'),
    path('currency-rates/', CurrencyRatesList.as_view(), name='currency-rates-list'),
    path('convert/', ConvertAmountView.as_view(), name='convert-amount'),
    path('historical/', HistoricalDataView.as_view(), name='historical-data'),

]

