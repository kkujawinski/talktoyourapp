import twilio.twiml
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from participants.models import Participant


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    data = request.POST
    try:
        phone_number = data['From']
        name = data['Body']
    except KeyError:
        return HttpResponseBadRequest()

    created = Participant.objects.update_name(phone_number, name)
    if created:
        msg = "Zarejestrowano Twój numer telefonu w konkursie pod nazwą '%s'." % name
    else:
        msg = "Zgłoszono zmianę nazwy na '%s'." % name

    resp = twilio.twiml.Response()
    resp.message(msg)
    return HttpResponse(str(resp))
