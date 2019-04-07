# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-03 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_book_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=255)),
                ('occupation_status', models.BooleanField()),
                ('postcode', models.CharField(max_length=50)),
                ('address_no', models.CharField(max_length=255)),
                ('address_street', models.CharField(max_length=255)),
                ('address_town', models.CharField(max_length=255)),
                ('authority_name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('floor_area', models.FloatField()),
                ('employee_count', models.FloatField()),
                ('rental_valuation', models.FloatField()),
                ('revenue', models.FloatField()),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]