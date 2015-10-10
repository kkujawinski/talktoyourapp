from django.db import models
from django.utils import timezone

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
    given_answer = models.ForeignKey(Answer, null=True)

    class Meta:
        unique_together = (
            ("participant", "given_answer"),
            ("participant", "question")
        )

    def __str__(self):
        return "%s %s" % (self.question, self.given_answer)


class Timer(models.Model):
    participant = models.OneToOneField(Participant)
    question_started = models.DateTimeField(null=True)
    time = models.FloatField(default=0)

    def start(self):
        self.question_started = timezone.now()
        self.save()

    def stop(self):
        q_time = timezone.now() - self.question_started()
        self.time += q_time.total_seconds()
        self.save()
