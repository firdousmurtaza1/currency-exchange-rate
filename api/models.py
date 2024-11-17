# -*- coding: utf-8 -*-
from django.db import models


class Currency(models.Model):
    """Represents a currency with a code, name, and symbol."""

    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


class CurrencyExchangeRate(models.Model):
    """Represents an exchange rate between two currencies on a specific date."""

    source_currency = models.ForeignKey(
        Currency, related_name="exchanges", on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(max_digits=18, decimal_places=6, db_index=True)

    class Meta:
        verbose_name = "Currency Exchange Rate"
        verbose_name_plural = "Currency Exchange Rates"

    def __str__(self):
        return f"{self.source_currency} to {self.exchanged_currency} on {self.valuation_date}: {self.rate_value}"

    @classmethod
    def create_from_provider(
        cls, source_currency, exchanged_currency, valuation_date, rate_value
    ):
        return cls.objects.create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date,
            rate_value=rate_value,
        )


class Provider(models.Model):
    """Represents a currency exchange rate provider with priority and activity status."""

    name = models.CharField(max_length=100)
    priority = models.PositiveIntegerField(
        default=1
    )  # Lower numbers have higher priority
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["priority"]
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    def __str__(self):
        return self.name
