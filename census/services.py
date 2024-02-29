import redis
import requests
import time
import json
import logging
import environ

from redis.commands.json.path import Path
from datetime import datetime

from . import models
from tasks.models import Partner, Task, Result, ResultData, WorkerComments

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)


_b2b = env('B2B')
_b2c = env('B2C')
_industrial = env('INDUSTRIAL')


def unix_to_date(unix):
    if unix is not None:
        date = str(unix)[:9]
        return datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d')
    else:
        return None


class DataInnOnRedis:
    def __init__(self):
        self.client = redis.Redis(host="localhost")
        self.dadata = env('DADATA_URL')

    def save_data(self, inn: str) -> dict | bool:

        headers: dict = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {env('DADATA_API_KEY')}"
        }

        data: dict = {"query": inn}

        r = requests.post(self.dadata, headers=headers, data=json.dumps(data))

        if r.status_code == 200:
            data: json = r.json()
            if len(data['suggestions']) > 0:
                new_data = self.client.json().set(inn, Path.root_path(), data['suggestions'])
                if new_data:
                    self.client.close()
                    return True
                else:
                    self.client.close()
                    return False
            else:
                return False
        else:
            return False

    def get_data(self, inn):
        data = self.client.json().get(inn)
        if data:
            self.client.close()
            return data
        else:
            self.client.close()
            return False

    def remove_data(self, inn):
        return self.client.delete(inn)


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
    _other_name = "Другое"
    request_files = request.FILES
    request = request.POST
    new_census = models.Census()
    new_census.address = request.get('address')
    new_census.department = models.Department.objects.get(name=request.get('depart'))
    new_census.name = request.get('name')
    task = Task.objects.get(number=request.get('guid'))
    new_census.task = task.number
    new_census.position = request.get('position')  # Координаты
    new_census.address_id = request.get('address_id')
    new_census.basics = task.base.number
    # new_census.edited = True
    print(request)

    # new_census.save()

    try:
        dadata = models.CompanyDatabase.objects.get(inn=request.get('inn'))
        new_census.dadata = dadata
    except models.CompanyDatabase.DoesNotExist:
        new_census.dadata = None

    if request.get('working'):
        new_census.working = Partner.objects.get(name=request.get('working'))
    else:
        pass

    new_census.point_name = request.get('point_name')  # Вывеска
    worker_comment = WorkerComments.objects.create(comment=request.get('result_comment'), worker_id=task.worker.pk)

    if request.get('closing') is not None:  # Если закрыто

        result = Result.objects.create(
            base_id=task.base.number,
            type='meet',
            result=ResultData.objects.get(name="АДРЕС НЕ АКТУАЛЕН"),
            task_number=task,
            contact_person="",
            control_date=None
        )
        new_census.result = result
        new_census.closing = True
        new_census.not_communicate = False
        new_census.save()

        if request_files:
            for file in request_files.getlist('file'):
                census_files = models.CensusFiles()
                census_files.census = new_census
                census_files.file = file
                census_files.save()

        Task.objects.filter(pk=task.pk).update(status='Выполнено', edited=True, result=result,
                                               worker_comment=worker_comment)
        return True

    elif request.get('not_communicate'):   # Если нет коммуникации

        result = Result.objects.create(
            base_id=task.base.number,
            type='meet',
            result=ResultData.objects.get(name="НЕТ КОНТАКТА"),
            task_number=task,
            contact_person="",
            control_date=None
        )

        new_census.not_communicate = True
        new_census.result = result
        new_census.closing = False
        new_census.save()

        Task.objects.filter(pk=task.pk).update(status='Выполнено', edited=True, result=result,
                                               worker_comment=worker_comment)

        return True

    else:

        control_date = None

        if len(request.get('control_date')) > 0:
            control_date = datetime.strptime(request.get('control_date'), '%d-%m-%Y')  # Если есть контрольная дата

        result = Result.objects.create(
            base_id=task.base.number,
            type='meet',
            result=ResultData.objects.get(code=request.get('result')),
            task_number=task,
            contact_person="",
            control_date=control_date
        )
        new_census.result = result

        new_census.category = models.PointCategory.objects.get(pk=request.get('category'))

        new_census.decision_firstname = request.get('firstname')
        new_census.decision_lastname = request.get('lastname')
        new_census.decision_surname = request.get('surname')
        new_census.decision_email = request.get('decision_email')
        new_census.decision_phone = request.get('decision_phone')
        new_census.decision_function = request.get('decision_function')

        new_census.save()

        #  сохранение направления
        for vector in models.PointVectors.objects.filter(pk__in=request.getlist('vectors')):

            if request.getlist(vector.slug):
                new_vector_item = models.PointVectorsItem.objects.create(
                    census=new_census,
                    vectors=vector,
                )
                for vector_pk in request.getlist(vector.slug):
                    new_value = models.PointVectorsSelectItem.objects.get(pk=vector_pk)
                    new_vector_item.value.add(new_value)
                for new_vector in models.PointVectorsItem.objects.filter(census__pk=new_census.pk):
                    new_census.vectors.add(new_vector)

            new_census.save()

        if request.get('depart') == _b2c:  # B2C

            new_census.nets = request.get('nets')
            new_census.point_type = models.PointTypes.objects.get(pk=request.get('point_type'))
            new_census.other_brand = request.get('other_brand')

            m2m_save(new_census.cars, models.CarsList.objects.filter(pk__in=request.getlist('cars')))

            if request.get('sto_type') is not None:
                new_census.sto_type = models.STOTypeList.objects.get(pk=request.get('sto_type'))

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

            try:
                if isinstance(int(request.get('lukoil_debit')), int):
                    new_census.lukoil_debit = request.get('lukoil_debit')
            except ValueError:
                new_census.lukoil_debit = 0

            try:
                if isinstance(int(request.get('rowe_debit')), int):
                    new_census.rowe_debit = request.get('rowe_debit')
            except ValueError:
                new_census.rowe_debit = 0

            try:
                if isinstance(int(request.get('motul_debit')), int):
                    new_census.motul_debit = request.get('motul_debit')
            except ValueError:
                new_census.motul_debit = 0

            try:
                if isinstance(int(request.get('vitex_debit')), int):
                    new_census.motul_debit = request.get('vitex_debit')
            except ValueError:
                new_census.motul_debit = 0

            try:
                if isinstance(int(request.get('elevators_count')), int):
                    new_census.elevators_count = request.get('elevators_count')
            except ValueError:
                new_census.elevators_count = 0

        elif request.get('depart') == _b2b or request.get('depart') == _industrial:  # B2B

            new_census.tender = request.get('tender')

            # Others
            new_others = models.Others.objects.create(census=new_census)
            try:
                other_eq = models.EquipmentList.objects.get(name=_other_name)
                new_others.equipment_name = request.get(f"equipment_other_name_{other_eq.pk}")

            except models.EquipmentList.DoesNotExist:
                new_others.equipment_name = None

            try:
                other_volume = models.Volume.objects.get(name=_other_name)
                new_others.volume_name = request.get(f'other_volume_name_{other_volume.pk}')
                new_others.volume_value = request.get(f'volume_{other_volume.pk}')

            except models.Volume.DoesNotExist:
                new_others.volume_name = None
                new_others.volume_value = None

            new_others.providers = request.get('other_providers')
            new_others.vector = request.get('other_vector')

            new_census.others = new_others
            new_others.save()

            for equipment in request.getlist('equipment'):
                new_equipment_item = models.EquipmentItem.objects.create(
                    census=new_census,
                    equipment=models.EquipmentList.objects.get(pk=equipment),
                    value=request.get(f'equipment_{equipment}')
                )
                new_census.equipment.add(new_equipment_item)

            #  сохранение объема
            for volume in request.getlist('volume'):
                new_volume_item = models.VolumeItem.objects.create(
                    census=new_census,
                    volume=models.Volume.objects.get(pk=volume),
                    value=request.get(f'volume_{volume}')
                )
                new_census.volume.add(new_volume_item)

        # m2m
        m2m_save(new_census.providers, models.ProviderList.objects.filter(pk__in=request.getlist('providers')))
        m2m_save(new_census.oils, models.OilList.objects.filter(pk__in=request.getlist('oils')))
        m2m_save(new_census.filters, models.FilterList.objects.filter(pk__in=request.getlist('filters')))
        m2m_save(new_census.vectors, models.PointVectorsItem.objects.filter(pk__in=request.getlist('vectors')))

        new_census.save()

        if request_files:
            for file in request_files.getlist('file'):
                census_files = models.CensusFiles()
                census_files.census = new_census
                census_files.file = file
                census_files.save()

        Task.objects.filter(pk=task.pk).update(status='Выполнено', edited=True, result=result,
                                               worker_comment=worker_comment)

        return True
