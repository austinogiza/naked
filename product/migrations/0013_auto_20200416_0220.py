# Generated by Django 3.0 on 2020-04-16 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20200416_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(max_length=50),
        ),
    ]
