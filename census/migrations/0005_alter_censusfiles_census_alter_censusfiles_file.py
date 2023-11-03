# Generated by Django 4.2.3 on 2023-11-01 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0004_censusfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censusfiles',
            name='census',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='census.census', verbose_name='Сенсус'),
        ),
        migrations.AlterField(
            model_name='censusfiles',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
