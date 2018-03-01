# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-01 08:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onmap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='position',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='position',
            name='pictures',
            field=models.ManyToManyField(related_name='positions', to='onmap.Picture'),
        ),
    ]
