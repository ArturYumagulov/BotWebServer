import json
from django.db.models import Q

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from core.tasks import save_organizations
from tasks.models import Partner, ResultData, PartnerWorker
from . import models
from .models import CompanyDatabase
from .services import valid_data, DataInnOnRedis


# Create your views here.


def template_test(request):
    return render(request, 'census/ready_census.html')


def census(request, pk):

    name = request.GET['name']
    city = request.GET['city']
    street = request.GET['street']
    house = request.GET['house']
    guid = request.GET['guid']
    categories = models.AccessoriesCategory.objects.filter(is_active=True).exclude(name="Другое")

    try:
        models.Census.objects.get(address_id=pk)
        return render(request, 'census/exist_census.html')

    except models.Census.DoesNotExist:

        context = {
            'name': name,
            'city': city,
            'street': street,
            'house': house,
            'address_id': pk,
            'guid': guid,
            'categories': categories
        }
        return render(request, 'census/census_form.html', context)


def load_data(request):
    form = valid_data(request)
    if form:
        return render(request, 'census/ready_census.html')
    else:
        return HttpResponse("<h1>Ошибка<h1>")
    # дописать валидацию и сохранение в БД


def get_partners(request):
    search_str = json.loads(request.body).get('searchText')
    partners = Partner.objects.filter(name__iregex=search_str)
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

    if request.method == 'GET':
        result = []
        point_names = models.PointTypes.objects.filter(is_active=True)
        for item in point_names:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_point_category(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        categories = models.PointCategory.objects.filter(is_active=True)
        for item in categories:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_sto_type(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        sto_types = models.STOTypeList.objects.filter(is_active=True)
        for item in sto_types:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_point_vector(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        point_vectors = models.PointVectors.objects.filter(is_active=True)
        for item in point_vectors:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_accessories_category(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        category = models.AccessoriesCategory.objects.filter(is_active=True)
        for item in category:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_accessories_category_item(request, category_id):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        items = models.AccessoriesCategoryItem.objects.filter(is_active=True).filter(category=category_id)
        for item in items:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_cars(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        cars = models.CarsList.objects.filter(is_active=True)
        for item in cars:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_oils(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        oils = models.OilList.objects.filter(is_active=True)
        for item in oils:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_filters(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        filters = models.FilterList.objects.filter(is_active=True)
        for item in filters:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_control_data(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        controls = ResultData.objects.filter(group__code="000000001")
        for item in controls:
            data = {'id': item.pk, 'name': item.name, 'control_data': item.control_data}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


def get_providers(request):
    """Категория точки"""

    if request.method == 'GET':
        result = []
        providers = models.ProviderList.objects.filter(is_active=True)
        for item in providers:
            data = {'id': item.pk, 'name': item.name}
            result.append(data)
        return JsonResponse(list(result), safe=False)

    return render(request, template_name='census/index.html')


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
