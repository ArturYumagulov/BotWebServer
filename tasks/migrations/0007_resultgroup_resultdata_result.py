# Generated by Django 4.0.3 on 2023-05-16 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ResultData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.resultgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('email', 'Электронное письмо'), ('phone', 'Телефонный звонок'), ('meet', 'Личная встреча'), ('e-market', 'Электронная торговая площадка'), ('postmail', 'Почтовое письмо'), ('other', 'Прочее')], default='other', max_length=1000)),
                ('result', models.CharField(max_length=1000)),
                ('contact_person', models.CharField(max_length=500)),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_bases', to='tasks.basics', verbose_name='Основание')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_groups', to='tasks.resultgroup')),
                ('task_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_task', to='tasks.task')),
            ],
        ),
    ]