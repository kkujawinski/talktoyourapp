# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20151005_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('participant', models.ForeignKey(to='participants.Participant')),
            ],
        ),
    ]
