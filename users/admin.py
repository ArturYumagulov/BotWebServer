from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserCodeDepartment


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserCodeDepartmentInline(admin.StackedInline):
    model = UserCodeDepartment
    can_delete = False
    verbose_name_plural = "employee"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserCodeDepartmentInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
