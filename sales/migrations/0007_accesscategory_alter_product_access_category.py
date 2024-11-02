# Generated by Django 4.2.3 on 2024-10-22 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_brand_alter_product_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=2000, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='access_category',
            field=models.ForeignKey(blank=True, max_length=1000, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.accesscategory', verbose_name='Категория товара'),
        ),
    ]
