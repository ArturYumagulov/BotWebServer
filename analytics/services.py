from census.models import Census
from tasks.models import Task


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


def create_volume_list(model):
    if model is not None:
        result = []
        for vol in model:
            item = dict()
            item['volume'] = vol.volume.name
            item['value'] = vol.value
            result.append(item)
        return result
    else:
        return None


def create_report_1(depart):
    data = []
    censuses = Census.objects.filter(department__name=depart).filter(address_id='5678')
    for census in censuses:
        res: dict = dict()
        res['author'] = census.task_author
        res['inn'] = census.inn
        res['name'] = census.name
        res['category'] = census.category.name
        res['result'] = census.task_result
        res['elevators'] = census.elevators_count
        res['equipments'] = create_equipment_list(census.equipmentitem_set.all())
        res['volumes'] = create_volume_list(census.volumeitem_set.all())

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
