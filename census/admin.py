from django.contrib import admin

from tasks.models import Task
from . import models
from .models import Census


# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'address', 'name', 'closing', 'created_date', 'edit_date', 'get_task_worker')
    readonly_fields = ('created_date', 'edit_date')
    fields = ('closing',
              'not_communicate',
              'department',
              'address_id',
              'created_date',
              'edit_date',
              'point_name',
              'point_type',
              'category',
              'providers',
              'nets',
              'sto_type',
              'cars',
              'oils',
              'filters',
              'accessories_category',
              'accessories_brands',
              'elevators_count',
              'oil_debit',
              'lukoil_debit',
              'rowe_debit',
              'motul_debit',
              'decision_firstname',
              'decision_lastname',
              'decision_surname',
              'decision_email',
              'decision_phone',
              'decision_function',
              'akb_specify',
              'working',
              'result',
              'task',
              'volume',
              'equipment',
              'tender',
              'position',
              'dadata',
              'vectors',
              'others'
              )

    def get_task_worker(self, obj):
        try:
            task = Task.objects.get(number=obj.task)
            return f"{task.worker}"
        except AttributeError:
            return "Удален"

    get_task_worker.short_description = "Исполнитель"


@admin.register(models.PointTypes)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PointVectors)
class PointVectorsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}


@admin.register(models.PointCategory)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CarsList)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OilList)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProviderList)
class ProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FilterList)
class FilterListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.STOTypeList)
class STOTypeListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AccessoriesCategory)
class AccessoriesCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AccessoriesCategoryItem)
class AccessoriesCategoryItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CensusFiles)
class CensusFilesAdmin(admin.ModelAdmin):

    list_display = ('pk', 'get_census_address', 'created_date', 'edited')

    def get_census_address(self, obj):
        return obj.census.address

    get_census_address.short_description = 'Адрес'


@admin.register(models.CompanyDatabase)
class CompanyDatabaseAdmin(admin.ModelAdmin):

    list_display = ('inn', 'status', 'value', 'created_date')
    search_fields = ('inn',)


@admin.register(models.Volume)
class VolumeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VolumeItem)
class VolumeItemAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.VolumeItemValue)
# class VolumeItemValueAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.EquipmentList)
class EquipmentListItemValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PointVectorsItem)
class PointVectorsItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PointVectorsSelectItem)
class PointVectorsSelectItemAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.EquipmentList)
# class EquipmentListAdmin(admin.ModelAdmin):
#     pass
