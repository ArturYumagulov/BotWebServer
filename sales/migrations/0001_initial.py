# Generated by Django 4.2.3 on 2024-05-30 09:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0011_partner_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('number', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Номер')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('sales_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата реализации')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.partner', verbose_name='Контрагент')),
            ],
            options={
                'verbose_name': 'Реализация',
                'verbose_name_plural': 'Реализации',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Код')),
                ('name', models.CharField(max_length=2000, verbose_name='Наименование')),
                ('article', models.CharField(blank=True, max_length=100, null=True, verbose_name='Артикул')),
                ('access_category', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Категория товара')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Номенклатуры',
                'verbose_name_plural': 'Номенклатура',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='RetailUnit',
            fields=[
                ('code', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='Код')),
                ('name', models.CharField(blank=True, max_length=2000, null=True)),
                ('category', models.CharField(blank=True, max_length=2000, null=True)),
                ('type', models.CharField(blank=True, max_length=2000, null=True)),
                ('address', models.CharField(max_length=2000, verbose_name='Адрес')),
                ('vector', models.CharField(max_length=2000, verbose_name='Направление')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Широта')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('contract', models.BooleanField(default=False)),
                ('partner_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.partner')),
            ],
            options={
                'verbose_name': 'Торговая точка',
                'verbose_name_plural': 'Торговые точки',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000, verbose_name='Наименование')),
                ('article', models.CharField(blank=True, max_length=100, null=True, verbose_name='Артикул')),
                ('access_category', models.CharField(max_length=1000, verbose_name='Категория товара')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, max_length=100, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField()),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.order')),
            ],
            options={
                'verbose_name': 'Позиция в реализации',
                'verbose_name_plural': 'Позиции в реализации',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='retail_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.retailunit', verbose_name='Торговая точка'),
        ),
    ]
