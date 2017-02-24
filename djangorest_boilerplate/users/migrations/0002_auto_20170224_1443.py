# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
    ]
