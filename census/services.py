from datetime import datetime

from django.shortcuts import get_object_or_404

from . import models
from tasks.models import Partner, Task, Result, ResultData, WorkerComments


def m2m_save(item, item_list):
    for i in item_list:
        item.add(i)


def get_valid(item):
    if len(item) == 0:
        return False
    else:
        return True


def get_integer_valid(item, data_item, value):
    var = item.get(value)
    if len(var) <= 0:
        data_item.value = 0
    else:
        if isinstance(int(var), int):
            data_item.value = int(var)
        else:
            data_item.value = 0
    return data_item.value


def valid_data(request):
    new_census = models.Census()
    new_census.address = request.get('address')
    new_census.name = request.get('name')
    task = Task.objects.get(number=request.get('guid'))
    new_census.task = task.number
    worker_comment = WorkerComments.objects.create(comment=request.get('result_comment'), worker_id=task.worker.pk)

    control_date = None

    if len(request.get('control_date')) > 0:
        control_date = datetime.strptime(request.get('control_date'), '%d-%m-%Y')

    if request.get('closing') is not None:  # Если закрыто

        result = Result.objects.create(
            base_id=task.base.number,
            type='meet',
            result=ResultData.objects.get(code="00000000099"),
            task_number=task,
            contact_person="",
            control_date=None
        )
        new_census.result = result
        new_census.address_id = request.get('address_id')
        new_census.closing = True
        new_census.save()

        Task.objects.filter(pk=task.pk).update(status='Выполнено', edited=True, result=result,
                                               worker_comment=worker_comment)
        return True

    else:

        result = Result.objects.create(
            base_id=task.base.number,
            type='meet',
            result=ResultData.objects.get(code=request.get('result')),
            task_number=task,
            contact_person="",
            control_date=control_date
        )
        new_census.result = result
        # foreign
        new_census.category = models.PointCategory.objects.get(pk=request.get('category'))
        new_census.point_type = models.PointTypes.objects.get(pk=request.get('point_type'))
        new_census.task = task.number
        new_census.point_type = models.PointTypes.objects.get(pk=request.get('point_type'))

        # required
        new_census.address_id = request.get('address_id')
        new_census.point_name = request.get('point_name')
        new_census.nets = request.get('nets')

        # null
        new_census.other_vector = request.get('other_vector')
        new_census.other_brand = request.get('other_brand')
        new_census.other_providers = request.get('other_providers')
        new_census.decision_fio = request.get('decision_fio')
        new_census.decision_email = request.get('decision_email')
        new_census.decision_phone = request.get('decision_phone')

        # hide

        # working
        if get_valid(request.get('working')):
            new_census.working = Partner.objects.get(name=request.get('working'))
        else:
            pass

        # sto_type
        if request.get('sto_type') is not None:
            new_census.sto_type = models.STOTypeList.objects.get(pk=request.get('sto_type'))
        else:
            pass

        # accessories_category
        if request.get('accessories_category') is not None:
            new_census.accessories_category = models.AccessoriesCategory.objects.get(
                pk=request.get('accessories_category')
            )
        else:
            pass

        try:
            if isinstance(int(request.get('oil_debit')), int):
                new_census.oil_debit = request.get('oil_debit')
        except ValueError:
            new_census.oil_debit = 0

        # lukoil_debit
        try:
            if isinstance(int(request.get('lukoil_debit')), int):
                new_census.lukoil_debit = request.get('lukoil_debit')
        except ValueError:
            new_census.lukoil_debit = 0
        # rowe_debit
        try:
            if isinstance(int(request.get('rowe_debit')), int):
                new_census.rowe_debit = request.get('rowe_debit')
        except ValueError:
            new_census.rowe_debit = 0
        # motul_debit
        try:
            if isinstance(int(request.get('motul_debit')), int):
                new_census.motul_debit = request.get('motul_debit')
        except ValueError:
            new_census.motul_debit = 0
        # elevators_count
        try:
            if isinstance(int(request.get('elevators_count')), int):
                new_census.elevators_count = request.get('elevators_count')
        except ValueError:
            new_census.elevators_count = 0

        new_census.save()

        # m2m
        m2m_save(new_census.providers, models.ProviderList.objects.filter(pk__in=request.getlist('providers')))
        m2m_save(new_census.cars, models.CarsList.objects.filter(pk__in=request.getlist('cars')))
        m2m_save(new_census.oils, models.OilList.objects.filter(pk__in=request.getlist('oils')))
        m2m_save(new_census.filters, models.FilterList.objects.filter(pk__in=request.getlist('filters')))
        m2m_save(new_census.accessories_brands, models.AccessoriesCategoryItem.objects.filter(
            pk__in=request.getlist('accessories_brands')
        ))
        m2m_save(new_census.vector, models.PointVectors.objects.filter(pk__in=request.getlist('vectors')))
        new_census.edited = True
        new_census.save()

        Task.objects.filter(pk=task.pk).update(status='Выполнено', edited=True, result=result,
                                               worker_comment=worker_comment)

        return True
