from django.contrib import admin

from tasks.models import Task
from . import models

# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'address', 'name', 'closing', 'created_date', 'edit_date', 'get_task_worker')
    readonly_fields = ('address_id', 'created_date', 'edit_date')
    fields = ('closing', 'address_id', 'created_date', 'edit_date', 'point_name', 'point_type', 'category', 'providers', 'vector', 'nets',
              'sto_type', 'cars', 'oils', 'filters', 'accessories_category', 'accessories_brands', 'elevators_count',
              'oil_debit', 'lukoil_debit', 'rowe_debit', 'motul_debit', 'decision_fio', 'decision_email',
              'decision_phone', 'other_brand', 'akb_specify', 'working', 'result', 'task')

    def get_task_worker(self, obj):
        task = Task.objects.get(number=obj.task.number)
        return f"{task.worker}"

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


# @admin.register(models.ProviderList)
# class CensusAdmin(admin.ModelAdmin):
#     pass
