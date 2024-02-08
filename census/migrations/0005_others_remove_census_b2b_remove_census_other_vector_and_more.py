# Generated by Django 4.2.3 on 2024-02-08 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0004_b2bothers_vector_alter_b2bothers_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Others',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Другой парк техники')),
                ('category', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Другая категория')),
                ('vector', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='')),
                ('volume', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Другой объем')),
                ('volume_value', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Другая категория')),
            ],
        ),
        migrations.RemoveField(
            model_name='census',
            name='b2b',
        ),
        migrations.RemoveField(
            model_name='census',
            name='other_vector',
        ),
        migrations.DeleteModel(
            name='B2BOthers',
        ),
        migrations.AddField(
            model_name='others',
            name='census',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='census_others', to='census.census'),
        ),
        migrations.AddField(
            model_name='census',
            name='others',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='census_others', to='census.others'),
        ),
    ]
