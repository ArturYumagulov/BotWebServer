from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ReportDownloadFile

# Register your models here.


@admin.register(ReportDownloadFile)
class ReportDownloadFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file')
    fields = ('user', 'elements', 'file')
    # readonly_fields = ('return_base_number_to_admin',)
    #
    # def return_base_number_to_admin(self, object):
    #     return mark_safe(f'<a target="_blank" href={object.path}>{object.path}<a>')
    #
    # return_base_number_to_admin.short_description = 'Путь'
