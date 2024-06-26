# Generated by Django 4.2.3 on 2024-02-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0005_others_remove_census_b2b_remove_census_other_vector_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='census',
            name='other_brand',
        ),
        migrations.RemoveField(
            model_name='census',
            name='other_providers',
        ),
        migrations.AddField(
            model_name='others',
            name='access_brand',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='others',
            name='providers',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='equipment',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='vector',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='volume',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='volume_value',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]
