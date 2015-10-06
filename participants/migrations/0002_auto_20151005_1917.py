# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='access_code',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='waiting_name',
        ),
        migrations.AlterField(
            model_name='participant',
            name='phone_number',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number needs to be in E.164 format', regex='^\\+[1-9]\\d{1,14}$')], max_length=16),
        ),
    ]
