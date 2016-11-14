# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServidorApp', '0006_auto_20161111_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connected_mobiles',
            name='user_fk',
            field=models.ForeignKey(to='ServidorApp.User'),
        ),
    ]
