# Generated by Django 4.0.3 on 2023-06-08 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_partnerworker_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='chat_id',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
