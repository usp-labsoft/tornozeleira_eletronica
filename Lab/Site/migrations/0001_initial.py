# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=11)),
                ('endereco', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=15)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('lat_max', models.FloatField()),
                ('lat_min', models.FloatField()),
                ('long_max', models.FloatField()),
                ('long_min', models.FloatField()),
            ],
        ),
    ]
