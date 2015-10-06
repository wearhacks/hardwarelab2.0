# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.PositiveIntegerField(default=0, blank=True)),
                ('serial_id', models.CharField(max_length=50)),
                ('device', models.ForeignKey(to='rental.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='checkoutdevice',
            name='user',
        ),
        migrations.DeleteModel(
            name='CheckoutDevice',
        ),
        migrations.AddField(
            model_name='deviceinventory',
            name='event',
            field=models.ManyToManyField(to='rental.Event'),
        ),
    ]
