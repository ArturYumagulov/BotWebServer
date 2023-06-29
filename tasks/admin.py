from django.contrib import admin
from . import models

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'date',
        'edited',
        'status',
        'deadline',
        'author',
        'worker',
        'base'
    )
    search_fields = [
        'author__name',
        'number',
        'base__number',
    ]
    list_filter = [
        'status'
    ]


class BaseAdmin(admin.ModelAdmin):
    # list_display = ('')
    search_fields = [
        'name',
        'number'
    ]


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
    )
    search_fields = [
        'name',
        'code'
    ]


class PartnerWorkersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'positions',
        'partner'
    )
    search_fields = [
        'partner__name',
        'partner__code'
    ]


class WorkersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'chat_id',
        'phone',
        'supervisor',
        'controller',
        'partner'
    )
    search_fields = [
        'name',
        'phone'
    ]
    list_filter = [
        'controller',
        'supervisor'
    ]


admin.site.register(models.Worker, WorkersAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Basics, BaseAdmin)
admin.site.register(models.AuthorComments)
admin.site.register(models.WorkerComments)
admin.site.register(models.Partner, PartnerAdmin)
admin.site.register(models.Result)
admin.site.register(models.ResultData)
admin.site.register(models.ResultGroup)
admin.site.register(models.PartnerWorker, PartnerWorkersAdmin)
admin.site.register(models.Supervisor)




