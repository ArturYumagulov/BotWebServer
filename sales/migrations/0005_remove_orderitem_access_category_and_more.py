# Generated by Django 4.2.3 on 2024-07-23 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_retailunit_address_alter_retailunit_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='access_category',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='article',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='name',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='sales.product', verbose_name='Товар'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активность'),
        ),
    ]
