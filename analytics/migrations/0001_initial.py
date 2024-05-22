# Generated by Django 4.2.3 on 2024-05-16 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('census', '0037_volume_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportOneFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.CharField(max_length=2000, verbose_name='id')),
                ('name', models.CharField(max_length=2000)),
                ('filter_field', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReportOneTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='census.department')),
                ('fields', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.reportonefields')),
            ],
        ),
    ]
