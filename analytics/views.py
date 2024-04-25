from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from analytics import services

# Create your views here.


# @login_required
def index(request):
    return render(request, 'analytics/report_1.html')


def report_1(request):
    data = services.create_report_1('industrial')
    return JsonResponse(
        {"data": data},
        safe=False
    )
