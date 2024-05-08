from django.contrib import admin

from .models import Course, Currency


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'value')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('char_code', 'name')
