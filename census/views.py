import json

import jwt
from django.db.models.functions import Lower
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from core.tasks import save_organizations
from tasks.models import Partner, ResultData, PartnerWorker, Worker, Task
from tasks.services import create_worker_secret
from . import models
from .models import CompanyDatabase, LukoilBrands, OilPackages
from .services import valid_data, DataInnOnRedis, clean_address

# Create your views here.

# departments
_b2b = 'b2b'
_b2c = 'b2c'
_industrial = 'industrial'


def template_test(request):
    return render(request, 'census/ready_census.html')


def census(request, pk):
    """Генерация страницы опросника"""

    if len(request.GET) > 0:

        depart = request.GET.get('depart')

        context = {
            'house': request.GET.get('house'),
            'address_id': pk,
            'depart': depart,
            'name': request.GET.get('name'),
            'city': request.GET.get('city'),
            'street': request.GET.get('street'),
            'guid': request.GET.get('guid'),
            'code': request.GET.get('code'),
            'chicago_code': request.GET.get('chicago'),
            'inn': request.GET.get('inn')
        }

        census_exists = models.Census.objects.filter(address_id=pk).exists()
        task_exist = Task.objects.filter(number=request.GET.get('guid')).exists()

        if census_exists or not task_exist:
            return render(request, 'census/exist_census.html')

        if depart == _b2b or depart == _industrial:

            products = models.PointVectors.objects \
                .filter(is_active=True) \
                .filter(department__name=_b2b)

            context['products'] = products

            return render(request, 'census/b2b.html', context)

        elif depart == _b2c:

            products = models.PointVectors.objects \
                .filter(is_active=True) \
                .filter(department__name=_b2c)

            volumes = models.Volume.objects.filter(is_active=True).filter(department__name='b2c')

            context['volumes'] = volumes
            context['products'] = products

            return render(request, 'census/b2c.html', context)

        return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')
    return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def full_census(request):

    depart = request.GET['depart']
    worker = request.GET['worker']
    token = request.GET['token']
    worker_data = Worker.objects.get(chat_id=worker)
    secret, algorithm = worker_data.secret.split('_')

    try:
        encode_worker_code = jwt.decode(token, secret, algorithms=algorithm)

        if worker_data.code == encode_worker_code['code']:
            products = models.PointVectors.objects \
                .filter(is_active=True) \
                .filter(department__name=depart)

            volumes = models.Volume.objects.filter(is_active=True).filter(department__name='b2c')

            context = {
                'depart': depart,
                'volumes': volumes,
                'products': products,
                'worker': worker
            }

            if depart == 'b2c':

                return render(request, 'census/b2c_census_template.html', context=context)

            elif depart == _b2b or depart == _industrial:

                return render(request, 'census/b2b_census_template.html', context=context)
            else:
                return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')

        else:
            return HttpResponse('census/errors/error_secret_code.html')

    except jwt.InvalidSignatureError:
        return render(request, 'census/errors/error_secret_code.html')


def load_data(request):
    """Запись результатов Сенсуса"""

    if request.method == "POST":
        try:
            models.Census.objects.get(address_id=request.POST.get('address_id'))
            return render(request, 'census/exist_census.html')

        except models.Census.DoesNotExist:
            form = valid_data(request)
            if form:
                return render(request, 'census/ready_census.html')
            return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')
    return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def full_load_data(request):
    """Запись результатов Сенсуса"""

    if request.method == "POST":

        form = valid_data(request, full=True)

        if form:
            return render(request, 'census/ready_census.html')
        else:
            return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')

    return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def get_partners(request):
    search_str = json.loads(request.body).get('searchText')
    partners = Partner.objects.filter(Q(name__icontains=search_str)|
                                      Q(inn__icontains=search_str)).distinct()
    return JsonResponse(list(partners.values()), safe=False)


def get_partners_inn(request):
    search_str = json.loads(request.body).get('searchInn')
    partners = Partner.objects.filter(inn=search_str)
    return JsonResponse(list(partners.values()), safe=False)


def get_partners_workers(request, partner_id):
    workers = PartnerWorker.objects.filter(partner__name=partner_id)
    return JsonResponse(list(workers.values()), safe=False)


def get_point_names(request):
    """Тип"""

    if request.method == 'POST':
        result = []
        point_names = models.PointTypes.objects.filter(is_active=True)
        for item in point_names:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_point_category(request):
    """Категория/Сегмент точки"""

    if request.method == 'POST':
        result = []
        categories = models.PointCategory.objects.order_by(Lower('name')).\
            filter(department__name=json.loads(request.body)['department']).filter(is_active=True)
        for item in categories:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(result, safe=False)

    return JsonResponse([{'detail': 'point_category not found'}], safe=False)


def get_sto_type(request):
    """Категория точки"""

    if request.method == 'POST':
        result = []
        sto_types = models.STOTypeList.objects.filter(is_active=True)
        for item in sto_types:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_point_vector(request):
    """Направление точки"""
    if request.method == 'POST':
        result = []
        point_vectors = models.PointVectors.objects.order_by(Lower('name')).\
            filter(department__name=json.loads(request.body)['department']).filter(is_active=True)
        for item in point_vectors:
            data = {'id': item.pk, 'name': item.name, 'slug': item.slug}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_accessories_category(request):
    """Категория точки"""

    if request.method == 'POST':
        result = []
        category = models.AccessoriesCategory.objects.filter(is_active=True)
        for item in category:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_accessories_category_item(request, category_id):
    """Категория точки"""
    if request.method == 'GET':
        result = []
        items = models.AccessoriesCategoryItem.objects.filter(is_active=True).filter(category=category_id)
        for item in items:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_cars(request):
    """Автомобили"""

    if request.method == 'POST':
        result = []
        cars = models.CarsList.objects.order_by(Lower('name')).filter(is_active=True)
        for item in cars:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_oils(request):
    """Категория точки"""

    if request.method == 'POST':
        result = []
        oils = models.OilList.objects.filter(is_active=True)
        for item in oils:
            data = {'id': item.pk, 'name': item.name, 'slug': item.slug}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_filters(request):
    """Категория точки"""

    if request.method == 'POST':
        result = []
        filters = models.FilterList.objects.filter(is_active=True)
        for item in filters:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_control_data(request):
    """Категория точки"""

    if request.method == 'POST':
        result = []
        controls = ResultData.objects.filter(group__name="Сенсус")
        for item in controls:
            data = {'id': item.pk, 'name': item.name, 'control_data': item.control_data}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'Not Found'}], safe=False)


def get_providers(request):
    """Поставщик точки"""

    if request.method == 'POST':
        result = []
        providers = models.ProviderList.objects.filter(department__name=json.loads(request.body)['department'])\
            .filter(is_active=True)
        for item in providers:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return JsonResponse([{'detail': 'providers not found'}], safe=False)


def get_inn(request):
    if request.method == "POST":
        result = []
        search_inn = json.loads(request.body).get('searchInn')
        organization_1C = Partner.objects.filter(inn=search_inn)

        if len(organization_1C) > 0:
            for organization in organization_1C:
                result.append({
                    'name': organization.name,
                    'inn': organization.inn,
                    'source': 'out'
                })
        else:
            try:
                organization = CompanyDatabase.objects.get(inn=search_inn)
                result.append({
                    'name': organization.value,
                    'inn': organization.inn,
                    'source': 'db'
                })

            except CompanyDatabase.DoesNotExist:
                organization = DataInnOnRedis().get_data(search_inn)
                if organization:
                    save_organizations.delay(search_inn)
                    if organization[0].get('value'):
                        result.append({
                            'name': organization[0]['value'],
                            'inn': organization[0]['data'].get('inn'),
                            'source': 'dadata'
                        })
                else:
                    if DataInnOnRedis().save_data(search_inn):
                        save_organizations.delay(search_inn)
                        organization = DataInnOnRedis().get_data(search_inn)[0]
                        if organization.get('value'):
                            result.append({
                                'name': organization['value'],
                                'inn': organization['data'].get('inn'),
                                'source': 'dadata'
                            })

        return JsonResponse(result, safe=False)


def get_volume_data(request):
    result = []
    if request.method == "POST":
        volumes = models.Volume.objects.filter(is_active=True).filter(department__name=json.loads(request.body)['department'])
        for volume in volumes:
            result.append({'id': volume.pk, 'name': volume.name})
        return JsonResponse(list(result), safe=False)
    return JsonResponse([{'detail': 'Volume Not Found'}], safe=False)


def get_equipment_park(request):
    result = []
    if request.method == "POST":
        equipments = models.EquipmentList.objects.order_by(Lower('name')).filter(is_active=True).filter(department__name=json.loads(request.body)['department'])
        for equipment in equipments:
            result.append({'id': equipment.pk, 'name': equipment.name})
        return JsonResponse(list(result), safe=False)
    return JsonResponse([{'detail': 'equipment Not Found'}], safe=False)


def get_vectors_items(request, slug):
    result = []
    if request.method == "POST":
        vectors_item = models.PointVectorsSelectItem.objects.order_by(Lower('name')).\
            filter(department__name=json.loads(request.body)['department']).filter(vectors__slug=slug)

        for item in vectors_item:
            data = {
                'id': item.pk,
                'name': item.name
            }
            result.append(data)
        return JsonResponse(list(result), safe=False, status=200)
    return JsonResponse({'result': 'vectors_item not found'}, safe=False, status=404)


@csrf_exempt
def clean_address_view(request):
    data = json.loads(request.body).get('address')
    result = clean_address(data)
    return JsonResponse(result, safe=False)


# def create_secret(request):
#     workers = Worker.objects.all()
#     for worker in workers:
#         worker.secret = create_worker_secret(token_len=44, algorithm='HS256')
#         worker.save()
#     return HttpResponse('ok')


def lukoil_brands_view(request):
    if request.method == "POST":
        result = []
        brands = LukoilBrands.objects.filter(is_active=True)
        for brand in brands:
            data = {
                'id': brand.pk,
                'name': brand.name,
                'slug': brand.slug
            }
            result.append(data)
        return JsonResponse(result, safe=False)


def package_volume(request):
    if request.method == "POST":
        result = []
        packages = OilPackages.objects.order_by('pk').filter(is_active=True)
        for package in packages:
            data = {
                'id': package.pk,
                'name': package.name,
                'slug': package.slug
            }
            result.append(data)
        return JsonResponse(result, safe=False)


def get_vectors_bonus_items(request):
    result = []
    if request.method == "POST":
        vectors_item = models.PointVectorsSelectItem.objects.order_by(Lower('name')).filter(bonuses=True).\
            filter(department__name=json.loads(request.body)['department'])

        for item in vectors_item:
            data = {
                'id': item.pk,
                'name': item.name
            }
            result.append(data)
        return JsonResponse(list(result), safe=False, status=200)
    return JsonResponse({'result': 'bonus not found'}, safe=False, status=404)
