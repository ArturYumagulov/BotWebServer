import json
from django.db.models.functions import Lower
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from core.tasks import save_organizations
from tasks.models import Partner, ResultData, PartnerWorker
from . import models
from .models import CompanyDatabase
from .services import valid_data, DataInnOnRedis, clean_address, valid_full_data

# Create your views here.

# departments
_b2b = 'b2b'
_b2c = 'b2c'
_industrial = 'industrial'


def template_test(request):
    return render(request, 'census/ready_census.html')


def census(request, pk):

    name = request.GET['name']
    city = request.GET['city']
    street = request.GET['street']
    house = request.GET['house']
    guid = request.GET['guid']
    depart = request.GET['depart']

    try:
        models.Census.objects.get(address_id=pk)
        return render(request, 'census/exist_census.html')

    except models.Census.DoesNotExist:

        if depart == _b2b or depart == _industrial:

            products = models.PointVectors.objects\
                .filter(is_active=True)\
                .filter(department__name=_b2b)

            context = {
                'name': name,
                'city': city,
                'street': street,
                'house': house,
                'address_id': pk,
                'guid': guid,
                'products': products,
                'depart': depart
            }
            return render(request, 'census/b2b.html', context)

        elif depart == _b2c:

            products = models.PointVectors.objects\
                .filter(is_active=True)\
                .filter(department__name=_b2c)

            volumes = models.Volume.objects.filter(is_active=True).filter(department__name='b2c')

            context = {
                'name': name,
                'city': city,
                'street': street,
                'house': house,
                'address_id': pk,
                'guid': guid,
                'products': products,
                'volumes': volumes,
                'depart': depart
            }
            return render(request, 'census/b2c.html', context)
        else:
            return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def full_census(request):

    depart = request.GET['depart']
    worker = request.GET['worker']

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

    return JsonResponse({'detail': 'add_template'})


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
            else:
                return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')

    return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def full_load_data(request):
    """Запись результатов Сенсуса"""

    if request.method == "POST":
        form = valid_full_data(request)

        if form:
            return render(request, 'census/ready_census.html')
        else:
            return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')

    return HttpResponse('<h1 style="text-align: center; margin: 20px;">Ошибка<h1>')


def get_partners(request):
    search_str = json.loads(request.body).get('searchText')
    partners = Partner.objects.filter(name__iregex=search_str).distinct()
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
