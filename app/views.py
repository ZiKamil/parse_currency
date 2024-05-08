from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render

from app.models import Course, Currency


def index(request):
    course_dates = Course.objects.only("date").values_list('date', flat=True).distinct()
    dates = []
    for date in course_dates:
        dates.append(date.strftime('%Y-%m-%d'))

    try:
        currencies = (
            Currency.objects.all()
            .prefetch_related("courses")
            .order_by("name")
        )
    except Currency.DoesNotExist:
        raise Http404("Currencies does not exist")
    context = {"currencies": currencies, "dates": dates}
    return render(request, "app/index.html", context)


def course(request):
    date = request.GET.get("date")
    try:
        currencies = (
            Currency.objects.all()
            .prefetch_related(
                Prefetch("courses", queryset=Course.objects.filter(date=date))
            )
            .order_by("name")
        )
    except Currency.DoesNotExist:
        raise Http404("Currencies does not exist")
    course_dates = Course.objects.only("date").values_list('date', flat=True).distinct()
    dates = []
    for date in course_dates:
        dates.append(date.strftime('%Y-%m-%d'))
    context = {"currencies": currencies, "dates": dates}
    return render(request, "app/index.html", context=context)
