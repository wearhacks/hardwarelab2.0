# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_auto_20151005_0354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceinventory',
            name='event',
        ),
        migrations.RemoveField(
            model_name='deviceinventory',
            name='stock',
        ),
        migrations.AddField(
            model_name='event',
            name='devices',
            field=models.ManyToManyField(to='rental.DeviceInventory'),
        ),
    ]
