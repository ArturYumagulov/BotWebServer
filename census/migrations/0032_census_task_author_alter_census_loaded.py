# Generated by Django 4.2.3 on 2024-04-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0031_census_loaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='task_author',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='census',
            name='loaded',
            field=models.BooleanField(default=False, verbose_name='Загружено'),
        ),
    ]
