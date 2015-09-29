from django.db import models
from django.core import validators


class Participant(models.Model):
    phone_number = models.CharField(
        max_length=16,
        validators=[
            validators.RegexValidator(
                regex='^\+[1-9]\d{1,14}$',
                message='Phone number needs to be in E.164 format',
                code='invalid_phone_number'
            ),
        ]
    )
    name = models.CharField(
        max_length=160,
        null=False
    )
    # Pranksters protection, name is not updated automatically if user is publicly visible
    waiting_name = models.CharField(
        max_length=160,
        null=True
    )
    accepted = models.BooleanField(default=False)
    access_code = models.CharField(max_length=4)
