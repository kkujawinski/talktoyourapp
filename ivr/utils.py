from questions.models import Question


def next_question(participant):
    answered = participant.givenanswer_set.values_list('question', flat=True)
    q = Question.objects.exclude(pk__in=answered)[:1]
    return q[0] if q else None
