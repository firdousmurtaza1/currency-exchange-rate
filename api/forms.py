# -*- coding: utf-8 -*-
from django import forms

from .models import Currency


class CurrencyConverterForm(forms.Form):
    """Repressent Custom Admin Form for conversion"""

    source_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(), label="Source Currency", required=True
    )
    amount = forms.DecimalField(
        label="Amount", max_digits=10, decimal_places=2, required=True
    )
    target_currencies = forms.ModelMultipleChoiceField(
        queryset=Currency.objects.all(), label="Target Currencies", required=True
    )
