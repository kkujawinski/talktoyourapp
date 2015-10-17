from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings

from participants.models import Participant
from questions.models import GivenAnswer
from ivr.models import CallEntry

from twilio.rest import TwilioRestClient


class GivenAnswerInline(admin.TabularInline):
    model = GivenAnswer
    fields = ('question', 'given_answer',)
    extra = 0
    max_num = 0
    readonly_fields = ('question', 'given_answer',)


class CallEntriesInline(admin.TabularInline):
    model = CallEntry
    fields = ('start_time', 'end_time',)
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False


class IsCallActiveListFilter(admin.SimpleListFilter):
    title = 'Is call active'
    parameter_name = 'is_call_active'

    def lookups(self, request, model_admin):
        return (
            (True, 'Yes'),
            (False, 'No'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val is None:
            return queryset
        ids = [item.id for item in queryset if str(item.is_call_active()) == val]
        return queryset.filter(id__in=ids)


def initiate_call_action(modeladmin, request, queryset):
    for participant in queryset:
        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
        )
        url = request.build_absolute_uri(
            reverse('ivr:welcome', kwargs={'participant_id': participant.id})
        )
        callback_url = request.build_absolute_uri(
            reverse('ivr:call_status')
        )
        url = url.replace('127.0.0.1:8000', 'b5973660.ngrok.io')
        callback_url = callback_url.replace('127.0.0.1:8000', 'b5973660.ngrok.io')

        client.calls.create(
            url=url,
            status_callback=callback_url,
            to=participant.phone_number,
            from_=settings.TWILIO_CALLING_NUMBER
        )

initiate_call_action.short_description = "Initiate lottery call"


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_call_active',)
    list_filter = (IsCallActiveListFilter,)
    inlines = (GivenAnswerInline, CallEntriesInline)
    actions = (initiate_call_action,)


admin.site.register(Participant, ParticipantAdmin)
