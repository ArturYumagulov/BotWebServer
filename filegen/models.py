import os

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class ReportDownloadFile(models.Model):
    elements = models.JSONField(null=True, verbose_name="Фильтрация")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    file = models.FileField(upload_to='reports/%Y/%m/%d/')

    def __str__(self):
        return str(self.pk)

