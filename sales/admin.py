from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models
from .resources import ProductResource


# Register your models here.


@admin.register(models.RetailUnit)
class RetailUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'article', 'access_category')
    list_filter = ('access_category',)
    fields = ('code', 'name', 'brand', 'article', 'access_category', 'tranzit_price', 'partkom_price', 'edit_date', 'created_date',)
    readonly_fields = ('edit_date', 'created_date',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('number', 'partner', 'retail_unit', 'edit_date', 'created_date',)
    readonly_fields = ('edit_date', 'created_date',)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AccessCategory)
class AccessCategoryAdmin(admin.ModelAdmin):
    pass
