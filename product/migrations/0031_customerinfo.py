# Generated by Django 3.0.5 on 2020-05-04 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20200503_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
    ]
