from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ivr.utils import next_question
from participants.models import Participant
from questions.models import Question, Answer, Timer
from twilio.rest import TwilioRestClient
from django.conf import settings
from twilio import twiml


VOICE = {'voice': 'alice', 'language': 'pl-PL'}


@csrf_exempt
@require_http_methods(["POST"])
def receive_call(request):
    try:
        phone_number = request.POST['From']
    except KeyError:
        return HttpResponseBadRequest()

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
@require_http_methods(["POST"])
def welcome(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    participant.start_call()
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
@require_http_methods(["POST"])
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
        correct_answers = participant.correct_answers
        summary_text = 'Prawidłowych odpowiedzi: %d. Twój czas to %d sekund.' % (
            correct_answers, int(participant.timer.time)
        )
        response.say(summary_text, **VOICE)
        # response.redirect(reverse('ivr:summary'))

    return HttpResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def answer(request, participant_id, question_id):
    participant = Participant.objects.get(id=participant_id)
    question = Question.objects.get(id=question_id)
    choice = request.POST.get('Digits')
    response = twiml.Response()

    Timer.objects.get(participant=participant).stop()

    if choice is not None:
        try:
            answers = Answer.objects.filter(
                question__id=question_id).order_by('pk')
            answer = answers[int(choice) - 1]
        except (IndexError, ValueError):
            participant.answer(question=question, answer=None)
        else:
            participant.answer(question=question, answer=answer)
    response.redirect(
        reverse('ivr:question', kwargs={'participant_id': participant.id})
    )
    return HttpResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def call_status(request):
    try:
        phone_number = request.POST['To']
    except KeyError:
        return HttpResponseBadRequest()
    participant = Participant.objects.get(phone_number=phone_number)
    participant.end_active_call()
    return HttpResponse()


def inititate(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
    )
    url = 'https://talktoyourapp.herokuapp.com/ivr/welcome/%d/' % participant.id
    callback_url = request.build_absolute_uri(
        reverse('ivr:call_status')
    )

    client.calls.create(
        url=url,
        status_callback=callback_url,
        to=participant.phone_number,
        from_=settings.TWILIO_CALLING_NUMBER
    )
    return HttpResponse()
