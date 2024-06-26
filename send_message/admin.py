from django.contrib import admin

from tasks.models import Worker
from .models import SendMessage

# Register your models here.


@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    fields = ('message', 'send_list', 'dont_send_list')
    readonly_fields = ('send_list', 'dont_send_list')



