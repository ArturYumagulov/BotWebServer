from django.contrib import admin

from vcard.models import VCard, Address


# Register your models here.

@admin.register(VCard)
class VCardAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass