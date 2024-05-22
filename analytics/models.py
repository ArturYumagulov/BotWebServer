from django.db import models
from census.models import Department


class ReportOneFields(models.Model):
    mid = models.CharField(max_length=2000, verbose_name='id')
    name = models.CharField(max_length=2000)
    filter_field = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ReportOneTable(models.Model):
    table_position = models.IntegerField(blank=True, null=True)
    depart = models.ForeignKey(Department, on_delete=models.PROTECT)
    fields = models.ForeignKey(ReportOneFields, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.depart} - {self.fields}'
