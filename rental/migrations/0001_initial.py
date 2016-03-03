# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import rental.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('image', models.ImageField(null=True, upload_to=rental.models.get_image_filename, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(help_text=b'ie: Short name, required field for event page: http://wearhacks.com/events/<slug>', blank=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('host', models.CharField(max_length=100, null=True)),
                ('devices', models.ManyToManyField(to='rental.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial_id', models.CharField(max_length=50)),
                ('rented', models.BooleanField(default=False)),
                ('device', models.ForeignKey(to='rental.Device')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reservation', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hack_finished', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('returned_at', models.DateTimeField(null=True, blank=True)),
                ('device', models.ForeignKey(to='rental.Device')),
                ('event', models.ForeignKey(to='rental.Event')),
                ('inventory', models.ForeignKey(blank=True, to='rental.Inventory', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comfort_level', models.IntegerField()),
                ('device_rating', models.IntegerField()),
                ('improvements', models.CharField(max_length=500)),
                ('other_comments', models.CharField(max_length=500)),
                ('devices', models.ManyToManyField(to='rental.Device')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to='rental.UserProfile'),
        ),
        migrations.AddField(
            model_name='event',
            name='inventories',
            field=models.ManyToManyField(to='rental.Inventory', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='managers',
            field=models.ManyToManyField(to='rental.Manager'),
        ),
        migrations.AddField(
            model_name='device',
            name='manufacturer',
            field=models.ForeignKey(default=0, to='rental.Manufacturer'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='inventory',
            order_with_respect_to='device',
        ),
    ]
