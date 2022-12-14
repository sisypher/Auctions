# Generated by Django 3.2.14 on 2022-09-28 02:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20220928_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='watchlisted', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 28, 4, 15, 17, 932645)),
        ),
    ]