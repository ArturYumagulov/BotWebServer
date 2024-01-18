# Generated by Django 4.2.3 on 2024-01-15 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0024_alter_census_volume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointcategory',
            options={'ordering': ['-created_date'], 'verbose_name': 'Категория/Сегмент торговой точки', 'verbose_name_plural': 'Категории/Сегмент торговых точек'},
        ),
        migrations.AlterModelOptions(
            name='pointvectors',
            options={'ordering': ['-created_date'], 'verbose_name': 'Направленность/Используемые продукты', 'verbose_name_plural': 'Направленность/Используемые продукты'},
        ),
        migrations.AddField(
            model_name='oillist',
            name='slug',
            field=models.SlugField(blank=True, default=None, null=True),
        ),
    ]