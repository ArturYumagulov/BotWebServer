# Generated by Django 4.2.3 on 2023-10-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_authorcomments_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='message_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
