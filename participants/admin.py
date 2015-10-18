from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings

from participants.models import Participant
from questions.models import Question, GivenAnswer
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
        try:
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
        except Exception:
            pass

initiate_call_action.short_description = "Initiate lottery call"


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_call_active', 'get_given_answers', 'correct_answers', 'timer',)
    list_filter = (IsCallActiveListFilter,)
    inlines = (GivenAnswerInline, CallEntriesInline)
    actions = (initiate_call_action,)

    def get_given_answers(self, obj):
        return obj.givenanswer_set.count()
    get_given_answers.short_description = 'Given answers'


admin.site.register(Participant, ParticipantAdmin)
