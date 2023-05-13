# Generated by Django 4.2 on 2023-05-13 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="worker",
            field=models.ForeignKey(
                default="Удален",
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="task_worker",
                to="tasks.worker",
                verbose_name="Исполнитель",
            ),
        ),
    ]
