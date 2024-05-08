from datetime import datetime

import requests
from django.core.management.base import BaseCommand

from app.models import Course, Currency
from parse_currency.settings import PARSE_URL


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        try:
            resp = requests.get(PARSE_URL)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        data: dict = resp.json()
        currencies: dict = data.get('Valute')

        currencies_list: list[Currency] = Currency.objects.all()
        currencies_names = [currency.name for currency in currencies_list]
        save_data = []
        for name, fields in currencies.items():
            if name not in currencies_names:
                save_data.append(Currency(
                    char_code=fields.get('CharCode'),
                    name=name,
                ))
        if save_data:
            try:
                currencies_list = Currency.objects.bulk_create(save_data)
            except Exception as e:
                raise f'False parse currency: {e}'

        currencies_objs = {currency.name: currency for currency in currencies_list}
        save_data = []
        for name, fields in currencies.items():
            date = datetime.fromisoformat(data.get("Date")).date()
            if not Course.objects.filter(date=date, currency=currencies_objs.get(name).pk).exists():
                save_data.append(Course(
                    currency=currencies_objs.get(name),
                    date=date,
                    value=fields.get("Value")
                ))
        try:
            Course.objects.bulk_create(save_data)
        except Exception as e:
            raise f'False parse course: {e}'

        self.stdout.write(
            self.style.SUCCESS('Successfully parse currency')
        )
