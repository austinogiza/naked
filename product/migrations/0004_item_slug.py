# Generated by Django 3.0 on 2020-04-14 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200414_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='product'),
            preserve_default=False,
        ),
    ]
