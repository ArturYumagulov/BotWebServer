# Generated by Django 4.2.3 on 2024-03-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0022_remove_census_accessories_brands_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='others',
            name='products',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]