# Generated by Django 4.0.3 on 2023-05-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_supervisor_worker_supervisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='controller',
            field=models.BooleanField(default=False),
        ),
    ]
