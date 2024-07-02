# Generated by Django 4.2.3 on 2024-07-01 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegen', '0006_alter_reportdownloadfile_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportdownloadfile',
            name='path',
        ),
        migrations.AddField(
            model_name='reportdownloadfile',
            name='file',
            field=models.FileField(default=1, upload_to='report/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
