# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20151005_1917'),
        ('questions', '0003_auto_20151006_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('question_started', models.DateTimeField(null=True)),
                ('time', models.FloatField(default=0)),
                ('participant', models.ForeignKey(unique=True, to='participants.Participant')),
            ],
        ),
        migrations.AlterField(
            model_name='givenanswer',
            name='given_answer',
            field=models.ForeignKey(to='questions.Answer', null=True),
        ),
    ]
