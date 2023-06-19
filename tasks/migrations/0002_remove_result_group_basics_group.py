# Generated by Django 4.0.3 on 2023-06-19 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='group',
        ),
        migrations.AddField(
            model_name='basics',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='basics_groups', to='tasks.resultgroup'),
            preserve_default=False,
        ),
    ]
