from census.models import Census, Volume, VolumeItem, AddressesCount
from sales.models import OrderItem
from tasks.models import Worker, Task, Department
from .models import ReportOneTable
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import pandas as pd
import numpy as np
import urllib.parse
import environ

env = environ.Env()
environ.Env.read_env()


# ------------------------Report 1------------------------

class Paginator:
    def __init__(self, items, items_per_page):
        self.items = items
        self.items_per_page = items_per_page
        self.total_pages = (len(items) + items_per_page - 1) // items_per_page

    def get_page(self, page_number):
        if 1 <= page_number <= self.total_pages:
            start_index = (page_number - 1) * self.items_per_page
            end_index = start_index + self.items_per_page
            return self.items[start_index:end_index]
        else:
            raise ValueError("Page number out of range")


def create_equipment_list(model):
    if model is not None:
        result = []
        for eq in model:
            result.append(f"{eq.equipment.name} {eq.value}")
        return result
    else:
        return None


def create_volume_list(model, depart):
    volumes = [vol.name for vol in Volume.objects.filter(is_active=True).filter(department__name=depart)]
    volume_items = [v.volume.name for v in model]
    if model is not None:
        result = []
        for volume in volumes:
            item: dict = dict()

            if volume in volume_items:
                vol = model.get(volume__name=volume)
                item['volume'] = volume
                item['value'] = vol.value
            else:
                item['volume'] = volume
                item['value'] = "0"
            result.append(item)
        return result
    else:
        return None


def create_volume_sum(volumes_list):
    item = {key['volume']: 0 for key in volumes_list}
    for i in volumes_list:
        item[i['volume']] += float(i['value'])
    return {'volumes': item}


def create_volumes(queryset):
    count = 0
    for i in queryset:
        if len(i) > 0:
            values_list = [float(x.value) for x in i.all()]
            count += sum(values_list)
    return count


def create_index_dict(dataframe_items):
    index_dict = {}
    for i in dataframe_items:
        index_dict[i[1]] = i[0]
    return index_dict


class ReportDataOnMongoDB:

    def __init__(self):
        self.username = urllib.parse.quote_plus(env('MONGO_USERNAME'))
        self.password = urllib.parse.quote_plus(env('MONGO_PASS'))

        self.client = client = MongoClient(
            host=f"mongodb://{self.username}:{self.password}@{env('MONGO_HOST')}",
            port=int(env('MONGO_PORT')))

        self.db = client['census_db']
        self.series_collection = self.db['census_collection']

    def insert_many_document(self, data: list):
        if len(data) > 0:
            self.series_collection.insert_many(data)
            return True
        else:
            return False

    def find_document(self, elements: dict | str = "", multiple: bool = False, all_item: bool = False,
                      summary=False, limit=100, skip=100) -> list:
        if all_item:
            results = self.series_collection.find({}, {'_id': 0})
            return [r for r in results]
        elif multiple:
            results = self.series_collection.find(elements, {'_id': 0}).limit(limit).skip(skip)
            res = [r for r in results]
            return res
        elif summary:
            results = self.series_collection.find(elements, {'_id': 0})
            res = [r for r in results]
            return res
        else:
            return self.series_collection.find_one(elements, {'_id': 0})

    def get_count(self, depart):
        return self.series_collection.count_documents(filter={'depart': depart})

    def volume_sum(self, depart):
        all_volume = []
        result = self.find_document(elements={'depart': depart, 'volumes.value': {'$gt': '0'}}, summary=True)
        volumes = [name.name for name in Volume.objects.filter(department__name=depart)]
        data = {key: 0 for key in volumes}
        for i in result:
            for ii in range(0, len(i['volumes'])):
                data[i['volumes'][ii]['volume']] += float(i['volumes'][ii]['value'])
                all_volume.append(float(i['volumes'][ii]['value']))
        return {'all_sum': sum(all_volume), 'defer': data}


def create_report_1(depart):
    data = []
    censuses = Census.objects.filter(department__name=depart).filter(loaded=False)
    all_volumes = [x.volumeitem_set.filter(volume__name='Общий') for x in censuses]
    we_oils = [x.volumeitem_set.exclude(volume__name='Общий') for x in censuses]
    all_volume_count = create_volumes(all_volumes)
    pot = create_volumes(we_oils)
    sub_pot_dict = {}
    pd.set_option('display.float_format', '{:.2f}'.format)

    for census in censuses:
        census_we_oils_include_join = [float(x.value) for x in census.volumeitem_set.exclude(volume__name="Общий")]
        try:
            if depart == 'industrial' or depart == 'b2b':
                sum_we_oils = int(census.others.all_volume)
            else:
                sum_we_oils = int(census.volumeitem_set.get(volume__name="Общий").value)
        except VolumeItem.DoesNotExist:
            sum_we_oils = 0
        except AttributeError:
            sum_we_oils = 0
        sum_we_oils_join = sum(census_we_oils_include_join)

        try:
            potential = int((sum_we_oils_join / pot) * 100)
            if potential == 0:
                potential = None
            sub_pot_dict[census.pk] = potential
        except ZeroDivisionError:
            sub_pot_dict[census.pk] = None

        dif = sum_we_oils - sum_we_oils_join

        def create_potential():
            try:
                count = round((dif / (all_volume_count - pot)) * 100)
            except ZeroDivisionError:
                count = 0
            if 20 < count > 70:
                return 1
            elif 20 < count > 10:
                return 2
            else:
                return 3

        res: dict = dict()
        res['_id'] = census.pk
        res['author'] = census.task_author
        res['depart'] = census.department.name
        res['worker'] = census.worker
        res['inn'] = census.inn
        res['name'] = census.name.replace('%20', ' ')
        res['result'] = census.task_result
        res['elevators'] = str(census.elevators_count)
        res['equipments'] = create_equipment_list(census.equipmentitem_set.all())
        res['volumes'] = create_volume_list(census.volumeitem_set.all(), census.department.name)
        res['diff'] = dif
        res['potential'] = str(create_potential())
        res['cars'] = [car.name for car in census.cars.all()]

        if census.category is None:
            res['segment'] = None
        else:
            res['segment'] = census.category.name

        if census.working is None:
            res['working'] = "Нет"
        else:
            res['working'] = "Да"

        if census.decision is None:
            res['contact'] = None
            res['phone'] = None
        else:
            res['contact'] = f"{census.decision.firstname} {census.decision.lastname} {census.decision.surname}"
            res['phone'] = f"{census.decision.phone}"

        data.append(res)
        census.loaded = True
        census.save()

    # ABC
    dataframe = pd.DataFrame(list(sub_pot_dict.items()), columns=['census_pk', 'category'])\
        .sort_values(ascending=False, by=['category'])
    dataframe['ABC'] = np.where(dataframe['category'] >= 70, 'A', np.where(dataframe['category'] >= 70, 'B', np.where(dataframe['category'] >= 20, 'B', "C")))
    dt = dataframe.to_dict()

    indexes = create_index_dict(dt['census_pk'].items())

    for i in data:
        i['category'] = dataframe['ABC'][indexes[i['_id']]]

    return data


def get_table_column(depart):
    table = []
    report_table = ReportOneTable.objects.filter(depart__name=depart).order_by('table_position')
    for report in report_table:
        data_dict: dict = dict()
        data_dict['id'] = report.fields.mid
        data_dict['name'] = report.fields.name
        data_dict['filter'] = report.fields.filter_field
        clear_data = data_dict.copy()
        table.append(clear_data)
        data_dict.clear()

    return table


def get_volumes_list(depart):
    result = []
    volumes = Volume.objects.filter(is_active=True).filter(department__name=depart)
    for item in volumes:
        data = {'id': item.pk, 'name': item.name, 'slug': item.slug}
        result.append(data)
    return result


def get_volume_sum_list(depart):
    return ReportDataOnMongoDB().volume_sum(depart)


# ------------------------Report 2------------------------
def amount_sum(partners_list):
    """
    Возвращает сумму всех заказов торговой точки.
    Принимает список контрагентов в задачах агента.
    """

    for partner in partners_list:
        sales = OrderItem.objects.filter(order__partner__code=partner)
        return sum([x.total for x in sales])


def create_report_2(dep_name):
    """Функция для создания данных второго отчета"""

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
                    ready_count_task = int(author_tasks.filter(status='Выполнено').count())
                    load_count_task = int(author_tasks.filter(status='Загружено').count())
                    ready_tasks = ready_count_task + load_count_task
                    partners = [x.working.code for x in active_clients if x.working.contract is not None]

                    result['department'] = dep_name
                    result['author'] = task.author.name
                    result['addresses'] = AddressesCount.objects.get(depart=dep_name).count
                    result['worker'] = task.worker.name
                    result['tasks'] = all_worker_task_count
                    result['ready_task'] = ready_tasks
                    result['active_task'] = active_tasks
                    result['active_clients'] = active_clients.count()

                    if potential_clients <= 0:
                        result['potential_clients'] = potential_clients
                    else:
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
    return result_list


if __name__ == '__main__':
    # gen_table_column('b2c')
    pass
