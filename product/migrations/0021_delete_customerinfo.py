# Generated by Django 3.0.5 on 2020-04-24 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_customerinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerInfo',
        ),
    ]
