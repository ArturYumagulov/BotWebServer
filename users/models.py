from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from tasks.models import Department


class UserCodeDepartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(verbose_name="Код 1С", max_length=11, blank=True, null=True)
