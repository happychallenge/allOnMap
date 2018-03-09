# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-08 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onmap', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='likes',
        ),
        migrations.AddField(
            model_name='position',
            name='plikes',
            field=models.ManyToManyField(related_name='poslikes', through='onmap.PLikes', to='onmap.IPaddress'),
        ),
        migrations.AlterField(
            model_name='plikes',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pp', to='onmap.Position'),
        ),
    ]
