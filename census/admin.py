from django.contrib import admin

from tasks.models import Task
from . import models
from .models import Census


# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):

    actions = ["make_load", "make_unload"]

    list_filter = ('department',)
    list_display = ('address_id', 'address', 'name', 'created_date', 'edit_date', 'department', 'loaded')
    readonly_fields = ('created_date', 'edit_date')
    fields = ('closing',
              'not_communicate',
              'loaded',
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

    @admin.action(description="Отменить загрузку Сенсуса")
    def make_load(self, request, queryset):
        queryset.update(loaded='False')

    @admin.action(description="Активировать загрузку Сенсуса")
    def make_unload(self, request, queryset):
        queryset.update(loaded='True')


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
    prepopulated_fields = {"slug": ('name',)}


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
    list_filter = ('is_active', 'vectors')
