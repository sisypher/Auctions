# Generated by Django 3.2.14 on 2022-10-08 19:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_created_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 8, 21, 46, 29, 213857)),
        ),
    ]
