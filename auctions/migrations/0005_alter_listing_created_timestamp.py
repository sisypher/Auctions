# Generated by Django 3.2.14 on 2022-09-27 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220927_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 15, 57, 11, 138614)),
        ),
    ]
