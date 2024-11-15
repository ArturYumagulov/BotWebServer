from import_export import resources, fields
from import_export import resources
from import_export.widgets import ManyToManyWidget

from .models import Census, EquipmentItem, PointVectorsItem, OilPackages, CarsList, ProviderList, PointVectorsSelectItem


class CensusResource(resources.ModelResource):
    equipments = fields.Field(
        column_name='equipment',  # Название столбца в файле
        attribute='equipment',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(EquipmentItem, separator=',', field='equipment')  # Указываем модель Genre и разделитель
    )
    vectors = fields.Field(
        column_name='vectors',  # Название столбца в файле
        attribute='vectors',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(PointVectorsItem, separator=',', field='vectors')  # Указываем модель Genre и разделитель
    )
    packages = fields.Field(
        column_name='packages',  # Название столбца в файле
        attribute='package',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(OilPackages, separator=',', field='name')  # Указываем модель Genre и разделитель
    )
    cars = fields.Field(
        column_name='cars',  # Название столбца в файле
        attribute='cars',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(CarsList, separator=',', field='name')
    )
    providers = fields.Field(
        column_name='providers',  # Название столбца в файле
        attribute='providers',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(ProviderList, separator=',', field='name')
    )
    lukoil_brands = fields.Field(
        column_name='lukoil_brands',  # Название столбца в файле
        attribute='lukoil_brands',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(ProviderList, separator=',', field='name')
    )
    bonuses = fields.Field(
        column_name='bonuses',  # Название столбца в файле
        attribute='bonuses',  # Название поля ManyToMany в модели
        widget=ManyToManyWidget(PointVectorsSelectItem, separator=',', field='name')
    )

    class Meta:
        model = Census
        fields = (
            'address_id',
            'address',
            'name',
            'department__name',
            'organizations_name',
            'tender',
            'task_author',
            'worker',
            'task_result',
            'point_name',
            'point_type__name',
            'nets',
            'sto_type__name',
            'category__name',
            'cars',
            'providers',
            'elevators_count',
            'decision__email',
            'akb_specify',
            'working__inn',
            'inn',
            'equipments',
            'closing',
            'not_communicate',
            'position',
            'vectors',
            'kpp',
            'packages',
            'federal',
            'lukoil_brands'
            'bonuses',
            'chicago_code',
            'code'
        )
