# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='givenanswer',
            name='question',
            field=models.ForeignKey(default=1, to='questions.Question'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='givenanswer',
            unique_together=set([('participant', 'given_answer')]),
        ),
    ]
