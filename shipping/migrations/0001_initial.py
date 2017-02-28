# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 19:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'((', max_length=50)),
                ('product', models.IntegerField(default=1)),
                ('mail_code', models.CharField(default=b'', max_length=100)),
                ('height', models.IntegerField(default=1)),
                ('length', models.IntegerField(default=1)),
                ('width', models.IntegerField(default=1)),
                ('weight', models.IntegerField(default=10)),
                ('value', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeliverableProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(default=b'', max_length=20)),
                ('height', models.IntegerField(default=16)),
                ('length', models.IntegerField(default=16)),
                ('width', models.IntegerField(default=16)),
                ('weight', models.FloatField(default=0.1)),
            ],
            options={
                'verbose_name_plural': 'Deliverable Properties',
            },
        ),
    ]
