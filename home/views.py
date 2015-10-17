from django.shortcuts import render
from django.conf import settings

from participants.models import Participant


def home(request):
    context = {'phone_number': settings.TWILIO_NUMBER, 'participants': Participant.objects.all()}
    return render(request, 'home/home.html', context=context)
