# Generated by Django 4.2.3 on 2024-07-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegen', '0002_remove_reportdownloadfile_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdownloadfile',
            name='path',
            field=models.CharField(max_length=10000, verbose_name='файл'),
        ),
    ]
