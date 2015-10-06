# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20151006_1946'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='givenanswer',
            unique_together=set([('participant', 'question'), ('participant', 'given_answer')]),
        ),
    ]
