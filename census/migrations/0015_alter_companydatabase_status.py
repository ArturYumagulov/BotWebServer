# Generated by Django 4.2.3 on 2023-11-13 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0014_remove_companydatabase_actuality_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydatabase',
            name='status',
            field=models.CharField(blank=True, choices=[('ACTIVE', 'действующая'), ('LIQUIDATING', 'ликвидируется'), ('LIQUIDATED', 'ликвидирована'), ('BANKRUPT', 'банкротство'), ('REORGANIZING', 'в процессе присоединения к другому юр.лицу, с последующей ликвидацией')], default=None, null=True, verbose_name='статус организации'),
        ),
    ]
