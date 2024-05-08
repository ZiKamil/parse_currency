from django.db import models


class Currency(models.Model):
    char_code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Валюты"


class Course(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="courses")
    date = models. DateField()
    value = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Курсы Валют"
