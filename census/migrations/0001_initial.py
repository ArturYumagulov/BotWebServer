# Generated by Django 4.2.3 on 2023-10-09 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0005_alter_task_options_alter_task_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessoriesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=1000, verbose_name='Категория аксессуаров')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список категорий аксессуаров',
                'verbose_name_plural': 'Списки категорий аксессуаров',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='AccessoriesCategoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Марка фильтра')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='census.accessoriescategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Список брендов в категории аксессуаров',
                'verbose_name_plural': 'Списки брендов в категории аксессуаров',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='CarsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Марка автомобиля')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список автомобилей торговой точки',
                'verbose_name_plural': 'Списки автомобилей торговой точки',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='FilterList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Марка фильтра')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список фильтров торговой точки',
                'verbose_name_plural': 'Списки фильтров торговой точки',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='OilList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Марка масла')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список масел торговой точки',
                'verbose_name_plural': 'Списки масел торговой точки',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='PointCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Имя категории')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Категория торговой точки',
                'verbose_name_plural': 'Категории торговых точек',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='PointTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Тип торговой точки')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='PointVectors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Имя направления торговой точки')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Направленность',
                'verbose_name_plural': 'Направленность',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ProviderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Марка масла')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список поставщиков торговой точки',
                'verbose_name_plural': 'Списки поставщиков торговой точки',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='STOTypeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
                ('name', models.CharField(max_length=500, verbose_name='Тип СТО')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'Список типов СТО торговой точки',
                'verbose_name_plural': 'Списки типов СТО торговой точки',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Census',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.PositiveBigIntegerField(verbose_name='ID адреса в 1С')),
                ('point_name', models.CharField(max_length=1000, verbose_name='Вывеска')),
                ('other_vector', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Другое направление')),
                ('nets', models.BooleanField(default=False, verbose_name='Сетевой')),
                ('elevators_count', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Количество подъемников')),
                ('oil_debit', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('lukoil_debit', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('rowe_debit', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('motul_debit', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('decision_fio', models.CharField(blank=True, max_length=2000, null=True, verbose_name='ЛПР_ФИО')),
                ('decision_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ЛПР_email')),
                ('decision_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('other_brand', models.TextField(blank=True, null=True, verbose_name='Другие бренды аксессуаров')),
                ('akb_specify', models.BooleanField(default=False, verbose_name='Специализированная точка по АКБ?')),
                ('edit_date', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('edited', models.BooleanField(default=False)),
                ('other_providers', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Другие поставщики')),
                ('accessories_brands', models.ManyToManyField(blank=True, default=None, to='census.accessoriescategoryitem', verbose_name='Бренды аксессуаров')),
                ('accessories_category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='census.accessoriescategory', verbose_name='Категории аксессуаров')),
                ('cars', models.ManyToManyField(blank=True, default=None, to='census.carslist', verbose_name='Автомобили обслуживают')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='census.pointcategory', verbose_name='Категория')),
                ('filters', models.ManyToManyField(blank=True, default=None, to='census.filterlist', verbose_name='Фильтры используют')),
                ('oils', models.ManyToManyField(blank=True, default=None, to='census.oillist', verbose_name='Масла используют')),
                ('point_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='census.pointtypes', verbose_name='Тип')),
                ('providers', models.ManyToManyField(to='census.providerlist', verbose_name='Основные поставщики')),
                ('result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.result', verbose_name='Результат встречи')),
                ('sto_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='census.stotypelist', verbose_name='Тип СТО')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tasks.task', verbose_name='Задача')),
                ('vector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='census.pointvectors', verbose_name='Направленность')),
                ('working', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tasks.partner', verbose_name='Контрагент в 1С')),
            ],
            options={
                'verbose_name': 'Сенсус',
                'verbose_name_plural': 'Сенсусы',
                'ordering': ['-created_date'],
            },
        ),
    ]
