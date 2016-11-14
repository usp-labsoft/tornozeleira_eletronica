# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0003_auto_20161104_0843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authentication',
            old_name='GPS',
            new_name='gps',
        ),
        migrations.RenameField(
            model_name='mobile_log',
            old_name='GPS',
            new_name='gps',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='CPF',
            new_name='cpf',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='connected_mobiles',
            name='phone',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
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
