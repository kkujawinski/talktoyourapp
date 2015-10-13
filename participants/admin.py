from django.contrib import admin

from participants.models import Participant
from questions.models import GivenAnswer
from ivr.models import CallEntry
from ivr.views import initiate_call


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
        initiate_call(request, participant)

initiate_call_action.short_description = "Initiate lottery call"


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_call_active',)
    list_filter = (IsCallActiveListFilter,)
    inlines = (GivenAnswerInline, CallEntriesInline)
    actions = (initiate_call_action,)


admin.site.register(Participant, ParticipantAdmin)
