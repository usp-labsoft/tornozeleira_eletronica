# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0007_auto_20161111_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authentication',
            old_name='mobile_log_id_fk',
            new_name='log_id_fk',
        ),
        migrations.AddField(
            model_name='authentication',
            name='log_source',
            field=models.CharField(default='Mobile', max_length=100),
            preserve_default=False,
        ),
    ]
