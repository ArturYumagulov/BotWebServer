# Generated by Django 4.2.3 on 2024-07-01 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegen', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportdownloadfile',
            name='file',
        ),
        migrations.AddField(
            model_name='reportdownloadfile',
            name='path',
            field=models.CharField(default=1, max_length=2000, verbose_name='файл'),
            preserve_default=False,
        ),
    ]