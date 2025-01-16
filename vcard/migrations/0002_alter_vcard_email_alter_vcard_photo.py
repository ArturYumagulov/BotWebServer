# Generated by Django 4.2.3 on 2025-01-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vcard',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='vcard',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='vcard_photos/'),
        ),
    ]
