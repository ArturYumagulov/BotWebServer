# Generated by Django 4.2.3 on 2024-02-08 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0009_remove_others_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='others',
            name='vector',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]