# Generated by Django 4.2.3 on 2023-11-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0006_census_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='decision_function',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Должность'),
        ),
    ]