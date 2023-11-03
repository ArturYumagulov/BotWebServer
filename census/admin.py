from django.contrib import admin

from tasks.models import Task
from . import models
from .models import Census


# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'address', 'name', 'closing', 'created_date', 'edit_date', 'get_task_worker')
    readonly_fields = ('address_id', 'created_date', 'edit_date')
    fields = ('closing', 'address_id', 'created_date', 'edit_date', 'point_name', 'point_type', 'category', 'providers', 'vector', 'nets',
              'sto_type', 'cars', 'oils', 'filters', 'accessories_category', 'accessories_brands', 'elevators_count',
              'oil_debit', 'lukoil_debit', 'rowe_debit', 'motul_debit', 'decision_fio', 'decision_email',
              'decision_phone', 'decision_function', 'other_brand', 'akb_specify', 'working', 'result', 'task',
              'position')

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
class CensusAdmin(admin.ModelAdmin):
    pass


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
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FilterList)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.STOTypeList)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AccessoriesCategory)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AccessoriesCategoryItem)
class CensusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CensusFiles)
class CensusFilesAdmin(admin.ModelAdmin):

    list_display = ('pk', 'get_census_address', 'created_date', 'edited')

    def get_census_address(self, obj):
        return obj.census.address

    get_census_address.short_description = 'Адрес'
