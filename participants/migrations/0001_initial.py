# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('phone_number', models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+[1-9]\\d{1,14}$', code='invalid_phone_number', message='Phone number needs to be in E.164 format')], max_length=16)),
                ('name', models.CharField(max_length=160)),
                ('waiting_name', models.CharField(max_length=160, null=True)),
                ('accepted', models.BooleanField(default=False)),
                ('access_code', models.CharField(max_length=4)),
            ],
        ),
    ]
