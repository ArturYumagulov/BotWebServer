# from django.db import models
#
# # Create your models here.
#
#
# class Providers(models.Model):
#     name = models.CharField(max_length=500, verbose_name="Название")
#     is_active = models.BooleanField(default=True, verbose_name="Активность")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = "Поставщик"
#         verbose_name_plural = "Поставщик"
