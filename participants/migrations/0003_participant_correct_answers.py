# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20151005_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='correct_answers',
            field=models.IntegerField(default=0),
        ),
    ]
