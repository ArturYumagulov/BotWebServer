from django.contrib import admin
from django.utils.safestring import mark_safe
from urllib.parse import unquote

from . import models

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        # 'number',
        'date',
        'edit_date',
        'edited',
        'deadline',
        'author',
        'worker',
        'return_base_number_to_admin',
        'return_result'
    )
    search_fields = [
        'author__name',
        'number',
        'base__number',
    ]
    list_filter = [
        'status'
    ]
    list_per_page = 20

    def return_base_number_to_admin(self, object):
        return mark_safe(f'<a href="/admin/tasks/basics/{object.base.number}/change/">{object.base.number}</a>')

    def return_result(self, object):
        result = object.result_task.all()
        for i in result:
            return mark_safe(f'<a href=/admin/tasks/result/{i.pk}/change/>{i.result}</a>')

    return_base_number_to_admin.short_description = 'Основание'
    return_result.short_description = "Результат"


class BaseAdmin(admin.ModelAdmin):
    # list_display = ('')
    search_fields = [
        'name',
        'number'
    ]
    list_per_page = 20


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
    )
    search_fields = [
        'name',
        'code'
    ]
    list_per_page = 20


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
    list_per_page = 20


class WorkersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_worker_urlencode',
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
    list_per_page = 20

    def get_worker_urlencode(self, object):
        url_decode = unquote(unquote(unquote(object.pk)))
        clean_code = unquote(unquote(url_decode))
        return mark_safe(f'<a href="/admin/tasks/worker/{clean_code}/change/">{clean_code}</a>')

    get_worker_urlencode.short_description = 'Агент'


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




