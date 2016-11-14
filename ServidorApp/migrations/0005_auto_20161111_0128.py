# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0004_auto_20161104_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lat_max',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lat_min',
        ),
        migrations.RemoveField(
            model_name='user',
            name='long_max',
        ),
        migrations.RemoveField(
            model_name='user',
            name='long_min',
        ),
    ]
