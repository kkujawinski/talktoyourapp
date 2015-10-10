# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20151010_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='participant',
            field=models.OneToOneField(to='participants.Participant'),
        ),
    ]
