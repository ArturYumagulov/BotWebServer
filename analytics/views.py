import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from analytics import services
from analytics.services import create_report_1
from census.models import Volume, Census, AddressesCount
from sales.models import OrderItem
from .services import get_table_column
from tasks.models import Task, Worker, Partner

# Create your views here.

User = get_user_model()


@login_required
def index(request):
    usr = User.objects.get(pk=request.user.pk)
    depart = usr.usercodedepartment.department
    context = {
        'b2c_column_list': get_table_column('b2c'),
        'industrial_column_list': get_table_column('industrial'),
        'b2b_column_list': get_table_column('b2b'),
        'depart': depart
    }
    return render(request, 'analytics/report_1.html', context)


@login_required
def report_2(request):
    usr = User.objects.get(pk=request.user.pk)
    depart = usr.usercodedepartment.department
    return render(request, 'analytics/report_2.html', {'depart': depart})


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
        return JsonResponse({'count': censuses}, safe=False)
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


def amount_sum(partners_list):
    for partner in partners_list:
        sales = OrderItem.objects.filter(order__partner__code=partner)
        return sum([x.total for x in sales])


@csrf_exempt
def get_report_2(requests):
    dep_name = json.loads(requests.body).get('depart')
    result_list = []

    workers_set = set(worker.code for worker in
                      Worker.objects.filter(department__name=dep_name))
    tasks = Task.objects.filter(base__group__name='Сенсус')
    author_lists = set(task.author.pk for task in tasks)

    for code in workers_set:
        for author in author_lists:
            author_tasks = tasks.filter(author__code=author).filter(worker__code=code)
            workers_list = set()
            for task in author_tasks:
                if task.worker.code not in workers_list:
                    result = {}
                    censuses = Census.objects.filter(worker=task.worker.name)
                    active_clients = censuses.filter(working__isnull=False)
                    potential_clients = censuses.filter(working__isnull=True).count()
                    all_worker_task_count = author_tasks.count()
                    active_tasks = author_tasks.filter(status='Новая').count()
                    ready_tasks = author_tasks.filter(status='Выполнено').count()
                    partners = [x.working.code for x in active_clients if x.working.contract is not None]

                    result['department'] = dep_name
                    result['author'] = task.author.name
                    result['addresses'] = AddressesCount.objects.get(depart=dep_name).count
                    result['worker'] = task.worker.name
                    result['tasks'] = all_worker_task_count
                    result['ready_task'] = ready_tasks
                    result['active_task'] = active_tasks
                    result['active_clients'] = active_clients.count()

                    result['potential_clients'] = \
                        f'<a style="text-decoration: none" ' \
                        f'href="/analytics/' \
                        f'?worker={task.worker.name}' \
                        f'&author={task.author.name}' \
                        f'&depart={dep_name}">{potential_clients}</a>'

                    result['contract'] = len(partners)
                    result['amount_sum'] = amount_sum(partners)
                    new_result = result.copy()
                    result_list.append(new_result)
                    workers_list.add(task.worker.code)
                    result.clear()

    return JsonResponse({'data': result_list}, safe=False)
