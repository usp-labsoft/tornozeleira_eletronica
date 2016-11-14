# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0005_auto_20161111_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lat_max',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='lat_min',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='long_max',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='long_min',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
