# Generated by Django 4.2.3 on 2024-07-01 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegen', '0005_alter_reportdownloadfile_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdownloadfile',
            name='path',
            field=models.CharField(max_length=10000),
        ),
    ]
