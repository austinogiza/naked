# Generated by Django 3.0.5 on 2020-04-22 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20200422_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='street_address',
            field=models.CharField(default='7 aguebor street', max_length=200),
            preserve_default=False,
        ),
    ]
