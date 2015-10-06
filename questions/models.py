from django.db import models

from participants.models import Participant


class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    correct = models.BooleanField()

    def __str__(self):
        return self.answer


class GivenAnswer(models.Model):
    participant = models.ForeignKey(Participant)
    question = models.ForeignKey(Question)
    given_answer = models.ForeignKey(Answer)

    class Meta:
        unique_together = (("participant", "given_answer"), ("participant", "question"))

    def __str__(self):
        return "%s %s" % (self.question, self.given_answer)
