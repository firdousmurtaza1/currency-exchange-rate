# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Currency, CurrencyExchangeRate


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    """Serializer for Currency Exchange Rate data."""

    class Meta:
        model = CurrencyExchangeRate
        fields = [
            "source_currency",
            "exchanged_currency",
            "valuation_date",
            "rate_value",
        ]


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency data."""

    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]
