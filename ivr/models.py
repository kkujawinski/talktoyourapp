from datetime import datetime
from django.db import models

from participants.models import Participant


class CallEntry(models.Model):
    participant = models.ForeignKey(Participant)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

    def end_call(self):
        self.end_time = datetime.now()
        self.save()

    def __str__(self):
        return "Call Entry"