from django.shortcuts import render
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta

from .models import MissionPerson, Mission, MissionVisualization, MissionSubmission
from .forms import SubmissionForm


def index(request):
    try:
        mission = Mission.objects.get(day=date.today())
    except Mission.DoesNotExist:
        mission = None
    cookie = request.session.get("uid", None)
    if cookie is None:
        person = MissionPerson(uid=uuid4())
        request.session["uid"] = str(person.uid)
    else:
        person = MissionPerson.objects.get(uid=UUID(cookie))
    if request.user.is_authenticated:
        person.user = request.user
    person.save()
    form = None
    if request.method == "GET" and mission:
        visualization, _ = MissionVisualization.objects.get_or_create(mission=mission, person=person)
        visualization.views.create(seen_at=datetime.now())
        visualization.save()
        form = SubmissionForm()
    elif request.method == "POST" and mission:
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.person = person
            submission.mission = mission
            submission.save()

    return render(request, template_name="missions/index.html", context={
        "mission": mission,
        "has_sent": person.has_sent,
        "next_mission": date.today() + timedelta(days=1),
        "form": form,
    })
