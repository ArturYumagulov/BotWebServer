# Generated by Django 4.2.3 on 2023-11-13 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0013_alter_companydatabase_liquidation_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companydatabase',
            name='actuality_date',
        ),
        migrations.RemoveField(
            model_name='companydatabase',
            name='liquidation_date',
        ),
        migrations.RemoveField(
            model_name='companydatabase',
            name='ogrn_date',
        ),
        migrations.RemoveField(
            model_name='companydatabase',
            name='registration_date',
        ),
    ]