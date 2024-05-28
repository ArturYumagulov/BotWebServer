import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from analytics import services
from analytics.services import create_report_1
from census.models import Volume, Census
from .services import get_table_column
from .models import ReportOneTable
from tasks.models import Task, Worker


# Create your views here.

User = get_user_model()


@login_required
def index(request):
    context = {
        'b2c_column_list': get_table_column('b2c'),
        'industrial_column_list': get_table_column('industrial'),
        'b2b_column_list': get_table_column('b2b')
    }
    return render(request, 'analytics/report_1.html', context)


@login_required
def report_2(request):
    return render(request, 'analytics/report_2.html')


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
def get_length(request):
    if request.method == "POST":
        depart = json.loads(request.body).get('depart')
        censuses = services.ReportDataOnMongoDB().get_count(depart)
        return JsonResponse({'count':  censuses}, safe=False)
    return JsonResponse({'error'}, safe=False)


@csrf_exempt
def get_volumes_sum(request):
    depart = json.loads(request.body).get('depart')
    data = services.ReportDataOnMongoDB().volume_sum(depart)
    return JsonResponse({'data': data})


def save_on_mongo(request):
    if services.ReportDataOnMongoDB().insert_many_document(create_report_1()):
        return HttpResponse('<h1>OK</h1>')
    return HttpResponse('<h1>Нет данных для сохранения</h1>')


@csrf_exempt
def get_report_2(requests):
    dep_name = json.loads(requests.body).get('depart')
    user_id = json.loads(requests.body).get('user_id')
    result_list = []
    user = User.objects.get(pk=user_id)
    workers_set = (worker.code for worker in Worker.objects.filter(department__name=dep_name).exclude(code=user.usercodedepartment.code))
    for code in workers_set:

        reports_length = Task.objects.filter(base__group__name='Сенсус').filter(worker__code=code).count()

        if reports_length > 0:
            result = {}
            worker = Worker.objects.get(code=code)
            all_worker_task = Task.objects.filter(base__group__name='Сенсус').filter(worker__code=code)
            censuses = Census.objects.filter(worker=worker.name)
            active_clients = censuses.filter(working__isnull=False).count()
            potential_clients = censuses.filter(working__isnull=True).count()
            all_worker_task_count = all_worker_task.count()
            active_tasks = all_worker_task.filter(status='Новая').count()
            ready_tasks = all_worker_task.filter(status='Выполнено').count()

            result['department'] = dep_name
            result['author'] = f"{user.first_name} {user.last_name}".strip()
            result['addresses'] = 5000
            result['worker'] = worker.name
            result['tasks'] = all_worker_task_count
            result['ready_task'] = ready_tasks
            result['active_task'] = active_tasks
            result['active_clients'] = active_clients
            result['potential_clients'] = potential_clients

            new_result = result.copy()
            result_list.append(new_result)
            result.clear()

    return JsonResponse({'data': result_list}, safe=False)
