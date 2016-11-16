# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0008_auto_20161116_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arduinos_time_log',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='authentication',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='mobile_log',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
