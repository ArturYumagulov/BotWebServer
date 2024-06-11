import environ
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model

from analytics import services
from analytics.services import create_report_2, create_report_1, get_volumes_list, get_volume_sum_list
from census.models import Volume
from tasks.models import Department
from .services import get_table_column
from .models import ReportUpdateModel

# Create your views here.

User = get_user_model()

env = environ.Env()
environ.Env.read_env()


_b2b = env('B2B')
_b2c = env('B2C')
_industrial = env('INDUSTRIAL')


@login_required
def index(request):
    usr = User.objects.get(pk=request.user.pk)
    depart = usr.usercodedepartment.department

    context = {

        f'{_b2c}_volume_sum_list': get_volume_sum_list(_b2c),
        f'{_b2b}_volume_sum_list': get_volume_sum_list(_b2b),
        f'{_industrial}_volume_sum_list': get_volume_sum_list(_industrial),

        'b2c_volume_list': get_volumes_list(_b2c),
        'b2b_volume_list': get_volumes_list('b2b'),
        'industrial_volume_list': get_volumes_list('industrial'),
        'b2c_column_list': get_table_column(_b2c),
        'industrial_column_list': get_table_column('industrial'),
        'b2b_column_list': get_table_column('b2b'),
        'depart': depart,
        'last_update': ReportUpdateModel.objects.last()
    }
    return render(request, 'analytics/report_1.html', context)


@login_required
def report_2(request):
    usr = User.objects.get(pk=request.user.pk)
    depart = usr.usercodedepartment.department
    return render(request, 'analytics/report_2.html', {'depart': depart})


def report_1(request):
    if request.method == "POST":
        limit = request.GET['limit']
        skip = request.GET['skip']
        depart = json.loads(request.body).get('depart')
        data = services.ReportDataOnMongoDB() \
            .find_document(
            elements={'depart': depart},
            multiple=True,
            limit=int(limit),
            skip=int(skip))
        return JsonResponse(
            {"data": data},
            safe=False
        )
    else:
        return {'method is get'}


def filter_report_1(request):
    if request.method == "POST":
        limit = request.GET['limit']
        skip = request.GET['skip']
        depart = json.loads(request.body).get('depart')
        filters = json.loads(request.body).get('filters')
        elements = {'depart': depart}
        if len(filters) > 0:

            for filter_item in filters:
                category = filter_item.split('_')[0]
                category_item = filter_item.split('_')[1]
                elements[category] = category_item

        data = services.ReportDataOnMongoDB().find_document(
            elements=elements,
            multiple=True,
            limit=int(limit),
            skip=int(skip))
        return JsonResponse({'data': data}, safe=False)
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
    return JsonResponse({'method is get'}, safe=False)


def get_length(request):
    if request.method == "POST":
        depart = json.loads(request.body).get('depart')
        censuses = services.ReportDataOnMongoDB().get_count(depart)
        return JsonResponse({'count': censuses}, safe=False)
    return JsonResponse({'error'}, safe=False)


def get_volumes_sum(request):
    depart = json.loads(request.body).get('depart')
    data = services.ReportDataOnMongoDB().volume_sum(depart)
    return JsonResponse({'data': data})


# def save_on_mongo(request):
#     departs = Department.objects.filter(is_active=True).exclude(name='director')
#     if len(departs) > 0:
#         for depart in departs:
#             new_status = ReportUpdateModel()
#             if services.ReportDataOnMongoDB().insert_many_document(create_report_1(depart.name)):
#                 new_status.name = depart.name
#                 new_status.date = datetime.datetime.now()
#                 new_status.depart = depart
#                 new_status.save()
#         return HttpResponse(f'<h1>OK</h1>')
#     return HttpResponse('<h1>Нет данных для сохранения</h1>')


def get_report_2(requests):

    dep_name = json.loads(requests.body).get('depart')
    result_list = create_report_2(dep_name)

    return JsonResponse({'data': result_list}, safe=False)
