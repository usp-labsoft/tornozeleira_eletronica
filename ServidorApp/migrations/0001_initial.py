# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arduinos_Time_Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('sensor_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Connected_Arduinos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('CPF', models.CharField(max_length=11)),
                ('picture', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='connected_arduinos',
            name='user',
            field=models.ForeignKey(to='ServidorApp.User'),
        ),
        migrations.AddField(
            model_name='arduinos_time_log',
            name='arduino_id',
            field=models.ForeignKey(to='ServidorApp.User'),
        ),
    ]
