from django.db import models
from django.core import validators


class ParticipantModelManager(models.Manager):
    def update_name(self, phone_number, name):
        participant, created = self.get_or_create(
            phone_number=phone_number, defaults={'name': name}
        )
        if not created:
            participant.name = name
            participant.save()


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

    def __str__(self):
        return '%s (...%s)' % (self.name, self.phone_number[-4:])