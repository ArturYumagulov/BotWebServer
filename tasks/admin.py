from django.contrib import admin
from django.utils.safestring import mark_safe
from urllib.parse import unquote

from . import models

# Register your models here.


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        # 'number',
        'date',
        'edit_date',
        'edited',
        'deadline',
        'partner',
        'return_author_num',
        'return_worker_num',
        'return_base_number_to_admin',
        'return_result'
    )
    search_fields = [
        'author__name',
        'number',
        'base__number',
    ]
    list_filter = [
        'base__group__name',
        'status',
        'worker',
    ]
    list_per_page = 20

    def return_base_number_to_admin(self, object):
        return mark_safe(f'<a href="/admin/tasks/basics/{object.base.number}/change/">{object.base.number}</a>')

    def return_result(self, object):
        result = object.result_task.all()
        for i in result:
            return mark_safe(f'<a href=/admin/tasks/result/{i.pk}/change/>{i.result}</a>')

    def return_worker_num(self, object):
        worker = object.worker
        return mark_safe(f'<a href="/admin/tasks/worker/{worker.code}/change/">{worker.name}</a>')

    def return_author_num(self, object):
        author = object.author
        return mark_safe(f'<a href="/admin/tasks/worker/{author.code}/change/">{author.name}</a>')

    return_base_number_to_admin.short_description = 'Основание'
    return_result.short_description = "Результат"
    return_worker_num.short_description = "Исполнитель"
    return_author_num.short_description = "Автор"


@admin.register(models.Basics)
class BaseAdmin(admin.ModelAdmin):
    # list_display = ('')
    search_fields = [
        'name',
        'number'
    ]
    list_per_page = 20


@admin.register(models.Partner)
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


@admin.register(models.PartnerWorker)
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


@admin.register(models.Worker)
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
        'phone',
        'chat_id'
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


@admin.register(models.ResultData)
class ResultDataAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'control_data', 'group',)
    list_filter = ('group',)


@admin.register(models.WorkerComments)
class WorkerCommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'worker', 'created_date')
    list_filter = ('worker',)


@admin.register(models.AuthorComments)
class AuthorCommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'created_date')
    list_filter = ('author',)


admin.site.register(models.Result)
admin.site.register(models.ResultGroup)
admin.site.register(models.Supervisor)
