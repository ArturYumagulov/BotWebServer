from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Worker)
admin.site.register(models.Task)
admin.site.register(models.Basics)
admin.site.register(models.AuthorComments)
admin.site.register(models.WorkerComments)
admin.site.register(models.Partner)

