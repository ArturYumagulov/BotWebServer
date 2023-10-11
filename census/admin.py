from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Census)
class CensusAdmin(admin.ModelAdmin):
    readonly_fields = ('address_id', 'created_date', 'edit_date')
    fields = ('address_id', 'created_date', 'edit_date', 'point_name', 'point_type', 'category', 'providers', 'vector', 'nets',
              'sto_type', 'cars', 'oils', 'filters', 'accessories_category', 'accessories_brands', 'elevators_count',
              'oil_debit', 'lukoil_debit', 'rowe_debit', 'motul_debit', 'decision_fio', 'decision_email',
              'decision_phone', 'other_brand', 'akb_specify', 'working', 'result', 'task')


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
