from census.models import Census
from tasks.models import Task
from census.models import Volume


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
            item = dict()
            item['equipments'] = eq.equipment.name
            item['value'] = eq.value
            result.append(item)
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


def create_car_list(model, depart):
    pass


def create_report_1(depart):
    data = []
    censuses = Census.objects.filter(department__name=depart) \
        # .filter(address_id='5678')
    for census in censuses:
        res: dict = dict()
        res['author'] = census.task_author
        res['inn'] = census.inn
        res['name'] = census.name.replace('%20', ' ')
        res['category'] = census.category.name
        res['result'] = census.task_result
        res['elevators'] = census.elevators_count
        res['equipments'] = create_equipment_list(census.equipmentitem_set.all())
        res['volumes'] = create_volume_list(census.volumeitem_set.all(), depart)
        res['cars'] = [car.name for car in census.cars.all()]

        if census.working is None:
            res['working'] = "Нет"
        else:
            res['working'] = "Да"

        if census.decision is not None:
            res['contact'] = f"{census.decision.firstname} {census.decision.lastname} {census.decision.surname}"
            res['phone'] = f"{census.decision.phone}"
        else:
            res['contact'] = None
            res['phone'] = None

        data.append(res)
    return data


if __name__ == '__main__':
    create_report_1('industrial')

    # Пример использования пагинатора
    items = list(range(1, 101))  # список чисел от 1 до 100
    paginator = Paginator(items, 10)  # создаем пагинатор для 10 элементов на страницу

    # Получаем элементы третьей страницы
    try:
        page_items = paginator.get_page(3)
        print("Items on page 3:", page_items)
    except ValueError as e:
        print(e)
