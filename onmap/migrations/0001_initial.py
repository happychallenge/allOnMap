# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-08 12:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IPaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(max_length=300, upload_to='uploads/%Y/%m/%d/')),
                ('name', models.CharField(max_length=300, verbose_name='My Name')),
                ('locname', models.CharField(max_length=300, verbose_name='LocationName')),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('lat', models.FloatField(blank=True, default=0, null=True)),
                ('lng', models.FloatField(blank=True, default=0, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onmap.IPaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='SLUG')),
                ('likes', models.IntegerField(default=0)),
                ('ptype', models.CharField(default='E', max_length=1, verbose_name='Type')),
                ('views', models.IntegerField(default=0)),
                ('public', models.BooleanField(default=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PositionPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onmap.Picture')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onmap.Position')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='pictures',
            field=models.ManyToManyField(related_name='positions', through='onmap.PositionPictures', to='onmap.Picture'),
        ),
        migrations.AddField(
            model_name='plikes',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onmap.Position'),
        ),
        migrations.AlterUniqueTogether(
            name='positionpictures',
            unique_together=set([('position', 'picture')]),
        ),
        migrations.AlterUniqueTogether(
            name='plikes',
            unique_together=set([('position', 'ipaddress')]),
        ),
    ]
