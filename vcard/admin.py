from django.contrib import admin

from vcard.models import VCard


# Register your models here.

@admin.register(VCard)
class VCardAdmin(admin.ModelAdmin):
    pass