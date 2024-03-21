from django.contrib import admin

from tasks.models import Task
from . import models
from .models import Census


# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):
    list_filter = ('department',)
    list_display = ('address_id', 'address', 'name', 'closing', 'created_date', 'edit_date', 'get_task_worker', 'department')
    readonly_fields = ('created_date', 'edit_date')
    fields = ('closing',
              'not_communicate',
              'inn',
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
              'elevators_count',
              'akb_specify',
              'working',
              'result',
              'task',
              'basics',
              'tender',
              'position',
              'dadata',
              )

    def get_task_worker(self, obj):
        try:
            task = Task.objects.get(number=obj.task)
            return f"{task.worker}"
        except AttributeError:
            return "Удален"

    get_task_worker.short_description = "Исполнитель"


@admin.register(models.PointTypes)
class PointTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.PointVectors)
class PointVectorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)
    prepopulated_fields = {"slug": ('name',)}


@admin.register(models.PointCategory)
class PointCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.CarsList)
class CarsListAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.ProviderList)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.STOTypeList)
class STOTypeListAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


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
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.EquipmentList)
class EquipmentListItemValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('department',)


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)


# PointVectorsSelectItem

@admin.register(models.PointVectorsSelectItem)
class PointVectorsSelectItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)