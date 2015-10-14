from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ivr.utils import next_question
from participants.models import Participant
from questions.models import Question, Answer, GivenAnswer, Timer

from twilio import twiml
from twilio.rest import TwilioRestClient


VOICE = {'voice': 'alice', 'language': 'pl-PL'}


def initiate_call(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
    )
    client.calls.create(
        url=request.build_absolute_uri(
            reverse('ivr:welcome', kwargs={'participant_id': participant.id})
        ),
        to=participant.phone_number,
        from_=settings.TWILIO_CALLING_NUMBER
    )
    return HttpResponse('ok!')


def receive_call(request):
    phone_number = request.POST['From']
    response = twiml.Response()
    response.pause(length=2)
    try:
        Participant.objects.get(phone_number=phone_number)
    except Participant.DoesNotExist:
        response.say(
            'Proszę zarejestrować się za pośrednictwem SMS.', **VOICE
        )
    else:
        response.say('Oddzwonimy, cierpliwości!', **VOICE)
    response.pause(length=2)
    response.hangup()
    return HttpResponse(response)


@csrf_exempt
def welcome(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    response = twiml.Response()
    response.pause(length=2)
    response.say(
        'Witaj {}. Czas na pytania!'.format(participant.name), **VOICE
    )
    response.redirect(
        reverse('ivr:question', kwargs={'participant_id': participant.id})
    )
    timer, created = Timer.objects.get_or_create(participant=participant)
    if created:
        timer.save()
    return HttpResponse(response)


@csrf_exempt
def question(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    response = twiml.Response()
    question = next_question(participant)

    if question:
        answers = Answer.objects.filter(question=question).order_by('pk')
        answers_txt = ' '.join([
            '{}) {}. \n'.format(i, answer.answer)
            for i, answer in enumerate(answers, 1)
        ])
        question_txt = '{} {}'.format(question.question, answers_txt)

        answer_url = reverse(
            'ivr:answer',
            kwargs={
                'participant_id': participant.id,
                'question_id': question.id
            }
        )

        timer = Timer.objects.get(participant=participant)
        timer.start()

        ask = response.gather(
            numDigits=1,
            action=answer_url,
            method='POST',
            timeout=30,
        )
        ask.say(question_txt, loop=5, **VOICE)

        response.say('Oooj...', **VOICE)  # Nie udzielono odpowiedzi. :(
        response.redirect(answer_url)

    else:
        response.say('To już wszystkie pytania.', **VOICE)
        # response.redirect(reverse('ivr:summary'))

    return HttpResponse(response)


@csrf_exempt
def answer(request, participant_id, question_id):
    participant = Participant.objects.get(id=participant_id)
    question = Question.objects.get(id=question_id)
    choice = request.POST.get('Digits')
    answer = None
    response = twiml.Response()

    Timer.objects.get(participant=participant).stop()

    if choice is not None:
        try:
            answers = Answer.objects.filter(
                question__id=question_id).order_by('pk')
            answer = answers[int(choice) - 1]
        except IndexError:
            pass

    GivenAnswer(
        participant=participant, question=question, given_answer=answer
    ).save()

    if answer and answer.correct:
        response.say('Brawo, prawidłowa odpowiedź!', **VOICE)
    else:
        response.say('Niestety, nieprawidłowa odpowiedź.', **VOICE)
    response.redirect(
        reverse('ivr:question', kwargs={'participant_id': participant.id})
    )

    return HttpResponse(response)


def on_call_end(request):
    phone_number = request.POST['From']
    participant = Participant.objects.get(phone_number=phone_number)
    participant.end_active_call()
