# Generated by Django 4.2.3 on 2024-10-22 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_accesscategory_alter_product_access_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='partkom_code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Код поставщика'),
        ),
    ]
