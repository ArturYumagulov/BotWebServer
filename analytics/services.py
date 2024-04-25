from census.models import Census
from tasks.models import Task


def create_report_1(depart):
    data = []
    censuses = Census.objects.filter(department__name=depart).filter(address_id='5678')
    for census in censuses:
        res: dict = dict()
        res['author'] = census.task_author
        res['inn'] = census.inn
        res['name'] = census.name
        res['category'] = census.category.name
        res['result'] = census.category.name
        res['elevators'] = census.elevators_count

        if census.equipmentitem_set.all() is not None:
            equipments_dict = []
            for eq in census.equipmentitem_set.all():
                item = dict()
                item['equipments'] = eq.equipment.name
                item['value'] = eq.value
                equipments_dict.append(item)

            res['equipments'] = equipments_dict
        else:
            res['equipments'] = None

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
