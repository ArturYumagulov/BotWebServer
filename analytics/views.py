import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analytics import services
from census.models import Volume

# Create your views here.


# @login_required
def index(request):
    return render(request, 'analytics/report_1.html')


@csrf_exempt
def report_1(request):
    if request.method == "POST":
        depart = json.loads(request.body).get('depart')
        data = services.create_report_1(depart)
        return JsonResponse(
            {"data": data},
            safe=False
        )
    else:
        return {'method is get'}


def get_volumes(request):
    if request.method == "POST":
        result = []
        depart = json.loads(request.body).get('depart')
        volumes = Volume.objects.filter(is_active=True).filter(department__name=depart)
        for item in volumes:
            data = {'id': item.pk, 'name': item.name, 'slug': item.slug}
            result.append(data)
        return JsonResponse(list(result), safe=False)
    else:
        return {'method is get'}

