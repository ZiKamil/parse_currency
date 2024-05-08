from datetime import datetime
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from app.models import Course, Currency


class CurrencyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(char_code='JPY', name='JPY')

    def test_char_code_label(self):
        currency = Currency.objects.get(id=1)
        field_label = currency._meta.get_field('char_code').verbose_name
        self.assertEqual(field_label, 'char code')

    def test_name_label(self):
        currency = Currency.objects.get(id=1)
        field_label = currency._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        currency = Currency.objects.create(char_code='JPY', name='JPY')
        Course.objects.create(currency=currency, date=datetime.now(), value=16.5)

    def test_date_label(self):
        currency = Course.objects.get(id=1)
        field_label = currency._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_name_label(self):
        currency = Course.objects.get(id=1)
        field_label = currency._meta.get_field('value').verbose_name
        self.assertEqual(field_label, 'value')


class ParseCurrencyAndCoursesTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command("parse", stdout=out)
        self.assertIn('Successfully parse currency', out.getvalue())
