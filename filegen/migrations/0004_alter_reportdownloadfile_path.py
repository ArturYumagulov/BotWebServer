# Generated by Django 4.2.3 on 2024-07-01 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegen', '0003_alter_reportdownloadfile_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdownloadfile',
            name='path',
            field=models.FilePathField(),
        ),
    ]
