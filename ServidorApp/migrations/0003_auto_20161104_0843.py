# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0002_remove_user_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('GPS', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('valid', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Connected_Mobiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_fk', models.ForeignKey(to='ServidorApp.Connected_Arduinos')),
            ],
        ),
        migrations.CreateModel(
            name='Mobile_Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('GPS', models.CharField(max_length=100)),
                ('auth_required', models.BooleanField()),
                ('mobile_id_fk', models.ForeignKey(to='ServidorApp.Connected_Mobiles')),
            ],
        ),
        migrations.RemoveField(
            model_name='arduinos_time_log',
            name='arduino_id',
        ),
        migrations.AddField(
            model_name='arduinos_time_log',
            name='arduino_id_fk',
            field=models.ForeignKey(default=1, to='ServidorApp.Connected_Arduinos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='authentication',
            name='mobile_log_id_fk',
            field=models.ForeignKey(to='ServidorApp.Mobile_Log'),
        ),
    ]
