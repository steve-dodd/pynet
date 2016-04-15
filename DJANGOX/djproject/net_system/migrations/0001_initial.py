# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('device_name', models.CharField(max_length=80, serialize=False, primary_key=True)),
                ('device_type', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('vendor', models.CharField(max_length=50, null=True, blank=True)),
                ('model', models.CharField(max_length=50, null=True, blank=True)),
                ('os_version', models.CharField(max_length=100, null=True, blank=True)),
                ('serial_number', models.CharField(max_length=50, null=True, blank=True)),
                ('uptime_seconds', models.IntegerField(null=True, blank=True)),
                ('credentials', models.ForeignKey(blank=True, to='net_system.Credentials', null=True)),
            ],
        ),
    ]
