# Generated by Django 3.0.5 on 2020-05-09 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_customerinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]