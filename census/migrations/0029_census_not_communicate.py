# Generated by Django 4.2.3 on 2024-01-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0028_pointvectorsitem_census_vectors'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='not_communicate',
            field=models.BooleanField(default=False, verbose_name='Нет коммуникации'),
        ),
    ]