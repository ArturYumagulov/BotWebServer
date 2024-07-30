from django.contrib import admin

from .models import ReportOneFields, ReportOneTable, ReportUpdateModel


@admin.register(ReportOneTable)
class ReportOneTableAdmin(admin.ModelAdmin):
    list_filter = ("depart",)
    list_display = ("table_position", "fields", "depart")
    ordering = ("table_position",)


@admin.register(ReportOneFields)
class ReportOneFieldsAdmin(admin.ModelAdmin):
    pass


@admin.register(ReportUpdateModel)
class ReportOneFieldsAdmin(admin.ModelAdmin):
    pass
