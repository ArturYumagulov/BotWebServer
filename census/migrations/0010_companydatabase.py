# Generated by Django 4.2.3 on 2023-11-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0009_censusfiles_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDatabase',
            fields=[
                ('inn', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='inn')),
                ('value', models.CharField(max_length=2000, verbose_name='Наименование компании')),
                ('kpp', models.CharField(blank=True, default=None, max_length=9, null=True, verbose_name='КПП')),
                ('ogrn', models.CharField(blank=True, default=None, max_length=13, null=True, verbose_name='ОГРН')),
                ('ogrn_date', models.DateField(blank=True, default=None, null=True, verbose_name='Дата выдачи ОГРН')),
                ('hid', models.CharField(max_length=2000, verbose_name='Внутренний идентификатор в Дадате')),
                ('type', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Тип организации')),
                ('full_with_opf', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Наименование компании')),
                ('short_with_opf', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Краткое наименование')),
                ('full', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Полное наименование без ОПФ')),
                ('short', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Краткое наименование без ОПФ')),
                ('fio_surname', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Фамилия ИП')),
                ('fio_name', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Имя ИП')),
                ('fio_patronymic', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Отчество ИП')),
                ('okato', models.CharField(blank=True, default=None, max_length=11, null=True, verbose_name='ОКАТО')),
                ('oktmo', models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name='ОКТМО')),
                ('okpo', models.CharField(blank=True, default=None, max_length=14, null=True, verbose_name='ОКПО')),
                ('okogu', models.CharField(blank=True, default=None, max_length=7, null=True, verbose_name='ОКОГУ')),
                ('okfs', models.CharField(blank=True, default=None, max_length=61, null=True, verbose_name='ОКФС')),
                ('okved', models.CharField(blank=True, default=None, max_length=61, null=True, verbose_name='ОКВЭД')),
                ('okved_type', models.CharField(blank=True, default=None, max_length=4, null=True, verbose_name='Версия справочника ОКВЭД (2001 или 2014)')),
                ('opf_code', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='код ОКОПФ')),
                ('opf_full', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='полное название ОПФ')),
                ('opf_short', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='краткое название ОПФ')),
                ('opf_type', models.CharField(blank=True, default=None, max_length=4, null=True, verbose_name='краткое название ОПФ')),
                ('management_name', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='ФИО руководителя')),
                ('management_post', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='должность руководителя')),
                ('branch_count', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Количество филиалов')),
                ('branch_type', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Тип подразделения')),
                ('address_value', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Адрес одной строкой')),
                ('address_unrestricted_value', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='адрес одной строкой (полный, с индексом)')),
                ('address_data', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='гранулярный адрес')),
                ('address_data_source', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='адрес одной строкой как в ЕГРЮЛ')),
                ('address_qc', models.CharField(blank=True, default=None, max_length=1, null=True, verbose_name='код проверки адреса')),
                ('actuality_date', models.DateField(blank=True, default=None, null=True, verbose_name='дата последних изменений')),
                ('registration_date', models.DateField(blank=True, default=None, null=True, verbose_name='дата последних изменений')),
                ('liquidation_date', models.DateField(blank=True, default=None, null=True, verbose_name='дата последних изменений')),
                ('status', models.DateField(blank=True, default=None, null=True, verbose_name='дата последних изменений')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
    ]