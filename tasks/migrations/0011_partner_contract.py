# Generated by Django 4.2.3 on 2024-05-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_alter_department_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='contract',
            field=models.BooleanField(default=False, verbose_name='Договор'),
        ),
    ]
