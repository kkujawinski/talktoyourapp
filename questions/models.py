from django.db import models

from participants import models as participants_models


class Question(models.Model):
    question = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    correct = models.BooleanField()


class GivenAnswer(models.Model):
    participant = models.ForeignKey(participants_models.Participant)
    given_answer = models.ForeignKey(Answer)
