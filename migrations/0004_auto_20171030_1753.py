# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_datamaster_master_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamaster',
            name='master_code',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='qrlabel',
            name='qrcode',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
    ]
