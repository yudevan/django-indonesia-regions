# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-23 03:25
from __future__ import unicode_literals, print_function
import os
import csv

from django.db import migrations, models
from django.db.utils import IntegrityError
import django.db.models.deletion

from djindonesiaregions.models import Province, Regency, District, Village

CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'csv'))


def populate_provinces(apps, schema_editor):
    print('\n\n  Populating provinces...')
    with open(os.path.join(CSV_PATH, 'provinces.csv'), 'rb') as provinces:
        reader = csv.reader(provinces, delimiter=b',')
        for i in reader:
            Province.objects.get_or_create(province_id=i[0], name=i[1])


def populate_regencies(apps, schema_editor):
    print('  Populating regencies...')
    with open(os.path.join(CSV_PATH, 'regencies.csv'), 'rb') as regencies:
        reader = csv.reader(regencies, delimiter=b',')
        for i in reader:
            try:
                province = Province.objects.get(province_id=i[1])
            except Province.DoesNotExist:
                print('Province %s not found.' % i[1])
            else:
                Regency.objects.get_or_create(name=i[2], regency_id=i[0],
                                              province=province)


def populate_districts(apps, schema_editor):
    print('  Populating districts...')
    with open(os.path.join(CSV_PATH, 'districts.csv'), 'rb') as disticts:
        reader = csv.reader(disticts, delimiter=b',')
        for i in reader:
            try:
                regency = Regency.objects.get(regency_id=i[1])
            except Regency.DoesNotExist:
                print('Regency %s not found.' % i[1])
            else:
                District.objects.get_or_create(name=i[2], district_id=i[0],
                                               regency=regency)


def populate_villages(apps, schema_editor):
    print('  Populating villages...')
    with open(os.path.join(CSV_PATH, 'villages.csv'), 'rb') as villages:
        reader = csv.reader(villages, delimiter=b',')
        for i in reader:
            try:
                district = District.objects.get(district_id=i[1])
            except District.DoesNotExist:
                print('District %s not found.' % i[1])
            else:
                Village.objects.get_or_create(name=i[2], village_id=i[0],
                                              district=district)
    print('  DONE.')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('district_id', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('province_id', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Regency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('regency_id', models.CharField(max_length=80, unique=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='djindonesiaregions.Province')),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('village_id', models.CharField(max_length=80, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='djindonesiaregions.District')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='regency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='djindonesiaregions.Regency'),
        ),
        migrations.RunPython(populate_provinces),
        migrations.RunPython(populate_regencies),
        migrations.RunPython(populate_districts),
        migrations.RunPython(populate_villages),
    ]
