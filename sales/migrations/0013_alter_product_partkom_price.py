# Generated by Django 4.2.3 on 2024-10-23 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_alter_product_edit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='partkom_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]