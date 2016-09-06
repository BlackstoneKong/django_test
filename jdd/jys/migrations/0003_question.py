# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-19 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jys', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField(max_length=10)),
                ('category_id', models.IntegerField(max_length=10)),
                ('subject', models.CharField(blank=True, max_length=500)),
                ('choice_a', models.CharField(blank=True, max_length=100)),
                ('choice_b', models.CharField(blank=True, max_length=100)),
                ('choice_c', models.CharField(blank=True, max_length=100)),
                ('choice_d', models.CharField(blank=True, max_length=100)),
                ('choice_e', models.CharField(blank=True, max_length=100)),
                ('choice_f', models.CharField(blank=True, max_length=100)),
                ('difficulty', models.CharField(blank=True, max_length=10)),
                ('answer', models.CharField(blank=True, max_length=2000)),
            ],
        ),
    ]
