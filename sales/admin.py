from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.RetailUnit)
class RetailUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'access_category')
    list_filter = ('access_category',)
    fields = ('name', 'article', 'access_category', 'price', 'edit_date', 'created_date',)
    readonly_fields = ('edit_date', 'created_date',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('number', 'partner', 'retail_unit', 'edit_date', 'created_date',)
    readonly_fields = ('edit_date', 'created_date',)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)
