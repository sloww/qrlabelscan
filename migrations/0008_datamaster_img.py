# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0007_scanrecord_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='datamaster',
            name='img',
            field=models.ImageField(default='pic/no-img.jpg', upload_to='pic/'),
        ),
    ]