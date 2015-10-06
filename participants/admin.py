from django.contrib import admin

from participants.models import Participant
from questions.models import GivenAnswer


class GivenAnswerInline(admin.TabularInline):
    model = GivenAnswer
    fields = ('question', 'given_answer',)
    extra = 0
    max_num = 0
    readonly_fields = ('question', 'given_answer',)


class ParticipantAdmin(admin.ModelAdmin):
    inlines = (GivenAnswerInline, )


admin.site.register(Participant, ParticipantAdmin)
