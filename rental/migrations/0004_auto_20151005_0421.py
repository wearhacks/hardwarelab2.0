# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0003_auto_20151005_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial_id', models.CharField(max_length=50)),
                ('device', models.ForeignKey(to='rental.Device')),
            ],
        ),
        migrations.RemoveField(
            model_name='deviceinventory',
            name='device',
        ),
        migrations.AlterField(
            model_name='event',
            name='devices',
            field=models.ManyToManyField(to='rental.Inventory'),
        ),
        migrations.DeleteModel(
            name='DeviceInventory',
        ),
    ]
