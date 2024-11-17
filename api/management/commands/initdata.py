# -*- coding: utf-8 -*-

"""
Initialize database with default data
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.consts import DefaultSuperUser
from api.models import Currency, Provider


class Command(BaseCommand):
    help = "Initialize default data"

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            self.stdout.write(
                self.style.NOTICE(
                    f"User database is empty, creating a default superuser: {DefaultSuperUser.NAME} / {DefaultSuperUser.PASSWORD}"
                )
            )
            User.objects.create_superuser(
                DefaultSuperUser.NAME, DefaultSuperUser.EMAIL, DefaultSuperUser.PASSWORD
            )

         # Currency data to be added
        currencies = [
            {"code": "GBP", "name": "Pound Sterling", "symbol": "£"},
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
        ]

        for currency_data in currencies:
            currency, created = Currency.objects.get_or_create(
                code=currency_data["code"],
                defaults={"name": currency_data["name"], "symbol": currency_data["symbol"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Currency {currency.name} created"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Currency {currency.name} already exists"))

        # Provider data to be added
        providers = [
            {"name": "CurrencyBeacon", "priority": 1, "is_active": True},
            {"name": "Mock", "priority": 2, "is_active": False},
        ]

        for provider_data in providers:
            provider, created = Provider.objects.get_or_create(
                name=provider_data["name"],  # Use 'name' for matching the provider
                defaults={"priority": provider_data["priority"], "is_active": provider_data["is_active"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Provider {provider.name} created"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Provider {provider.name} already exists"))

        
