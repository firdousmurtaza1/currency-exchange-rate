# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, reverse

from api.models import Currency, CurrencyExchangeRate, Provider
from api.views import CurrencyConverterAdminView


# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol")  # Display relevant fields


@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "source_currency",
        "exchanged_currency",
        "rate_value",
        "valuation_date",
    )


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "is_active")  # Customize as needed


# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    # site_header = "MyCurrency Admin"
    # site_title = "Currency Management"
    # index_title = "Welcome to the MyCurrency Admin Panel"

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        # Add custom link to the context
        extra_context["custom_links"] = [
            {
                "name": "Currency Converter",
                "url": reverse("admin:currency_converter"),
            }
        ]
        return super().index(request, extra_context=extra_context)

    # Add custom URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "currency-converter/",
                self.admin_view(CurrencyConverterAdminView.as_view()),
                name="currency_converter",
            ),
        ]
        return custom_urls + urls


# Register your custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

# Register models with the custom admin site
custom_admin_site.register(Currency, CurrencyAdmin)
custom_admin_site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
custom_admin_site.register(Provider, ProviderAdmin)
