from django.db import models
from django.db.models.loading import get_model
from django.core import validators


class ParticipantModelManager(models.Manager):
    def update_name(self, phone_number, name):
        participant, created = self.get_or_create(
            phone_number=phone_number, defaults={'name': name}
        )
        if not created:
            participant.name = name
            participant.save()
        return created


class Participant(models.Model):
    objects = ParticipantModelManager()

    phone_number = models.CharField(
        max_length=16,
        validators=[
            validators.RegexValidator(
                regex='^\+[1-9]\d{1,14}$',
                message='Phone number needs to be in E.164 format',
                code='invalid_phone_number'
            ),
        ],
        unique=True
    )
    name = models.CharField(
        max_length=160,
        null=False
    )
    correct_answers = models.IntegerField(default=0)

    def answer(self, question, answer):
        GivenAnswer = get_model('questions', 'GivenAnswer')
        GivenAnswer(
            participant=self, question=question, given_answer=answer
        ).save()

        self.correct_answers = self.givenanswer_set.filter(given_answer__correct=True).count()
        self.save()

    def is_call_active(self):
        return bool(self._get_active_call())
    is_call_active.boolean = True

    def start_call(self):
        CallEntry = get_model('ivr', 'CallEntry')
        self.callentry_set.filter(end_time__isnull=True).delete()
        CallEntry.objects.create(participant=self)

    def end_active_call(self):
        callentry = self._get_active_call()
        if callentry:
            callentry.end_call()

    def _get_active_call(self):
        CallEntry = get_model('ivr', 'CallEntry')
        try:
            return self.callentry_set.get(end_time__isnull=True)
        except CallEntry.DoesNotExist:
            pass

    def __str__(self):
        return '%s (...%s)' % (self.name, self.phone_number[-4:])
