import redis
import requests
import json
import logging
import environ
import jwt
from django.conf import settings

from redis.commands.json.path import Path
from datetime import datetime

from . import models
from tasks.models import Partner, Task, Result, ResultData, WorkerComments, Worker
from .models import Census

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)


_b2b = env("B2B")
_b2c = env("B2C")
_industrial = env("INDUSTRIAL")
token = env.str("BOT_TOKEN")


def unix_to_date(unix):
    if unix is not None:
        date = str(unix)[:9]
        return datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    else:
        return None


class DataInnOnRedis:
    def __init__(self):
        self.client = redis.Redis(host="localhost")
        self.dadata = env("DADATA_URL")

    def save_data(self, inn: str) -> dict | bool:

        headers: dict = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {env('DADATA_API_KEY')}",
        }

        data: dict = {"query": inn}

        r = requests.post(self.dadata, headers=headers, data=json.dumps(data))

        if r.status_code == 200:
            data: json = r.json()
            if len(data["suggestions"]) > 0:
                new_data = self.client.json().set(
                    inn, Path.root_path(), data["suggestions"]
                )
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


def del_ready_task(request, task):
    r = requests.get(
        f"https://api.telegram.org/bot{token}/deleteMessage?chat_id={task.worker.chat_id}&message_id={task.message_id}"
    )
    if r.json()["ok"]:
        logger.info(
            f"{task.number}- {r.json()['result']} - " f"- удалено сообщение - 201"
        )
        return True
    else:
        logger.error(f"{task.number} - {r.json()['description']}" f"- не удалено - 400")
        return False


def save_files(filelist, census_model):

    for file in filelist.getlist("file"):
        census_files = models.CensusFiles()
        census_files.census = census_model
        census_files.file = file
        census_files.save()


def save_tasks(task, worker_comment, result):

    result = Result.objects.create(
        base_id=task.base.number,
        type="meet",
        result=ResultData.objects.filter(group__code="000000004").get(name=result),
        task_number=task,
        contact_person="",
        control_date=None,
    )

    Task.objects.filter(pk=task.pk).update(
        status="Выполнено",
        edited=True,
        result=result,
        worker_comment=worker_comment,
    )

    return result


def return_data_on_dadata(inn):
    if inn is not None:
        try:
            dadata = models.CompanyDatabase.objects.get(inn=inn)
            return dadata
        except models.CompanyDatabase.DoesNotExist:
            return None
    return None


def create_decisions(request, census_model):

    new_decisions = models.Decision.objects.create(
        census=census_model,
        firstname=request.get("firstname"),
        lastname=request.get("lastname"),
        surname=request.get("surname"),
        email=request.get("decision_email"),
        phone=request.get("decision_phone"),
        function=request.get("decision_function"),
    )

    new_decisions.save()
    return new_decisions


class CensusSave:
    """Класс работы с моделью Сенсуса"""
    def __init__(self, request):

        self._other_name = "Другое"
        self.request = request.POST
        self.request_files = request.FILES

        self.new_census = Census()
        self.task = Task.objects.get(number=self.request.get("guid"))
        self.new_census.address = self.request.get("address")
        self.new_census.department = models.Department.objects.get(name=self.request.get("depart"))
        self.new_census.name = self.request.get("name")
        self.new_census.task = self.task.number
        self.new_census.position = self.request.get("position")
        self.new_census.address_id = self.request.get("address_id")
        self.new_census.basics = self.task.base.number
        self.new_census.inn = self.request.get("inn")
        self.new_census.task_author = self.task.author.name
        self.new_census.worker = self.task.worker.name
        self.new_census.edited = True
        self.worker_comment = WorkerComments.objects.create(
            comment=self.request.get("result_comment"), worker_id=self.task.worker.pk
        )
        if self.request.get("working"):
            self.new_census.working = Partner.objects.get(inn=str(self.request.get("working")))

    def closing_point(self, result_status):
        result = save_tasks(self.task, self.worker_comment, result_status)
        self.new_census.result = result
        self.new_census.task_result = result.result.name
        self.new_census.save()

        save_files(self.request_files, self.new_census)

        del_ready_task(self.request, self.task)

    def not_communicate(self):
        self.new_census.not_communicate = True

    def point_closing(self):
        self.new_census.closing = True

    def working_point(self):

        self.new_census.dadata = return_data_on_dadata(self.request.get("inn"))
        self.new_census.category = models.PointCategory.objects.get(
            pk=self.request.get("category")
        )
        result = save_tasks(self.task, self.worker_comment, "ДАННЫЕ АКТУАЛИЗИРОВАНЫ")
        self.new_census.result = result
        self.new_census.task_result = result.result.name
        self.new_census.save()

        # Сохранение контактного лица
        self.new_census.decision = create_decisions(self.request, self.new_census)

        # Сохранение направления точки
        for vector in models.PointVectors.objects.filter(
            pk__in=self.request.getlist("vectors")
        ):
            if self.request.getlist(vector.slug):
                new_vector_item = models.PointVectorsItem.objects.create(
                    census=self.new_census,
                    vectors=vector,
                )
                for vector_pk in self.request.getlist(vector.slug):
                    new_value = models.PointVectorsSelectItem.objects.get(pk=vector_pk)
                    new_vector_item.value.add(new_value)
                for new_vector in models.PointVectorsItem.objects.filter(
                    census__pk=self.new_census.pk
                ):
                    self.new_census.vectors.add(new_vector)

            self.new_census.save()

    def b2c_point(self):
        """Если точка B2C"""

        self.new_census.nets = self.request.get("nets")
        self.new_census.point_type = models.PointTypes.objects.get(
                pk=self.request.get("point_type")
            )
        self.new_census.other_brand = self.request.get("other_brand")

        if self.request.get("elevators_count"):
            self.new_census.elevators_count = int(self.request.get("elevators_count"))

        m2m_save(
            self.new_census.cars,
            models.CarsList.objects.filter(pk__in=self.request.getlist("cars")),
        )
        m2m_save(
            self.new_census.providers,
            models.ProviderList.objects.filter(pk__in=self.request.getlist("providers")),
        )

        if self.request.get("sto_type"):
            self.new_census.sto_type = models.STOTypeList.objects.get(
                pk=self.request.get("sto_type")
            )

        if self.request.get("akb_specify"):
            self.new_census.akb_specify = int(self.request.get("akb_specify"))

        new_others = models.Others.objects.create(census=self.new_census)
        new_others.vector = self.request.get("other_vector")
        new_others.providers = self.request.get("other_providers")
        new_others.save()

        self.new_census.others = new_others

        oil = models.PointVectors.objects.get(name="Масло")
        debit_items = models.Volume.objects.filter(is_active=True).filter(
            department__name=_b2c
        )

        if str(oil.pk) in self.request.getlist("vectors"):
            for volume in debit_items:
                new_volume_item = models.VolumeItem.objects.create(
                    census=self.new_census,
                    volume=models.Volume.objects.get(pk=volume.pk),
                    value=self.request.get(f"volume_{volume.pk}"),
                )
                self.new_census.volume.add(new_volume_item)

        self.new_census.save()

        del_ready_task(self.request, self.task)

    def b2b_point(self):
        """Если точка B2B или Индустриальный отдел"""
        self.new_census.tender = self.request.get("tender")

        # Others
        new_others = models.Others.objects.create(census=self.new_census)
        try:
            other_eq = models.EquipmentList.objects.get(name=self._other_name)
            new_others.equipment_name = self.request.get(
                f"equipment_other_name_{other_eq.pk}"
            )

        except models.EquipmentList.DoesNotExist:
            new_others.equipment_name = None

        try:
            other_volume = models.Volume.objects.get(name=self._other_name)
            new_others.volume_name = self.request.get(
                f"other_volume_name_{other_volume.pk}"
            )
            new_others.volume_value = self.request.get(f"volume_{other_volume.pk}")

        except models.Volume.DoesNotExist:
            new_others.volume_name = None
            new_others.volume_value = None

        new_others.providers = self.request.get("other_providers")
        new_others.vector = self.request.get("other_vector")
        new_others.all_volume = self.request.get("all_volume")

        self.new_census.others = new_others
        new_others.save()

        # Парк техники
        for equipment in self.request.getlist("equipment"):
            new_equipment_item = models.EquipmentItem.objects.create(
                census=self.new_census,
                equipment=models.EquipmentList.objects.get(pk=equipment),
                value=self.request.get(f"equipment_{equipment}"),
            )
            self.new_census.equipment.add(new_equipment_item)

        #  сохранение объема
        for volume in self.request.getlist("volume"):
            new_volume_item = models.VolumeItem.objects.create(
                census=self.new_census,
                volume=models.Volume.objects.get(pk=volume),
                value=self.request.get(f"volume_{volume}"),
            )
            self.new_census.volume.add(new_volume_item)

        m2m_save(
            self.new_census.providers,
            models.ProviderList.objects.filter(pk__in=self.request.getlist("providers")),
        )
        m2m_save(
            self.new_census.vectors,
            models.PointVectorsItem.objects.filter(pk__in=self.request.getlist("vectors")),
        )

        self.new_census.save()


def valid_data(request):

    new_census = CensusSave(request=request)

    if request.POST.get("closing") is not None:  # Если закрыто
        new_census.point_closing()
        new_census.closing_point(result_status="АДРЕС НЕ АКТУАЛЕН")
        return True

    elif request.POST.get("not_communicate"):  # Если нет коммуникации
        new_census.not_communicate()
        new_census.closing_point(result_status="НЕТ КОНТАКТА")
        return True

    elif request.POST.get("depart") == _b2c:
        new_census.working_point()
        new_census.b2c_point()
        return True

    elif request.POST.get("depart") == _b2b or request.POST.get("depart") == _industrial:
        new_census.working_point()
        new_census.b2b_point()
        return True


def clean_address(address):
    headers: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {env('DADATA_API_KEY')}",
        "X-Secret": env("DADATA_SECRET"),
    }
    data = json.dumps([address])
    r = requests.post(url=env("DADATA_CLEAN_ADDRESS_URL"), headers=headers, data=data)
    if r.status_code == 200:
        return r.json()
        # return r.json()[0]['result']
    else:
        return None


ALGORITHM = "HS256"


def token_generator(user):
    return jwt.encode(user, settings.SECRET_KEY, algorithm=ALGORITHM)
