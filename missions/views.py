from django.shortcuts import render
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required
import pytz

from engajaflix.settings import TIME_ZONE

from .models import MissionPerson, Mission, MissionVisualization, MissionSubmission
from .forms import SubmissionForm


def get_mission(request, year=None, month=None, day=None):
    user_agent = get_user_agent(request)
    can_share = not user_agent.is_pc and user_agent.os.family != "iOS"

    if year is None:
        now = datetime.now(pytz.timezone(TIME_ZONE))
        midnight = (now + timedelta(days=1)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        next_mission = (midnight - now).seconds
    else:
        now = datetime.fromisoformat(f"{year:04}-{month:02}-{day:02}")
        next_mission = None
    try:
        mission = Mission.objects.get(day=now.date())
    except Mission.DoesNotExist:
        mission = None
    cookie = request.session.get("uid", None)
    if cookie is None:
        person = MissionPerson(uid=uuid4())
        request.session["uid"] = str(person.uid)
    else:
        person, _ = MissionPerson.objects.get_or_create(uid=UUID(cookie))
    if request.user.is_authenticated:
        person.user = request.user
    person.save()
    form = None
    if request.method == "GET" and mission:
        visualization, _ = MissionVisualization.objects.get_or_create(mission=mission, person=person)
        visualization.views.create(seen_at=now)
        visualization.save()
        form = SubmissionForm(initial={"name": request.user.get_full_name(), "email": request.user.email})
    elif request.method == "POST" and mission:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.person = person
            submission.mission = mission
            submission.save()

    if mission and person:
        completed = mission.missionsubmission_set.filter(person=person).count()
        mission_number = mission.number
    else:
        completed = 0
        mission_number = ""

    share_text = (
        gettext_lazy("I completed mission #") +
        f"{mission_number}! {completed} " +
        gettext_lazy("missions completed so far!") +
        " https://engajaflix.club/"
    )

    if mission and person:
        submission = MissionSubmission.objects.filter(person=person, mission=mission).first()
    else:
        submission = None
    return render(request, template_name="missions/get.html", context={
        "mission": mission,
        "next_mission": next_mission,
        "can_share": can_share,
        "share_text": share_text,
        "form": form,
        "person": person,
        "submission": submission
    })


@login_required
def list_missions(request):
    now = datetime.now(pytz.timezone(TIME_ZONE))
    person = MissionPerson.objects.filter(user=request.user).first()
    if person.on_class:
        missions = person.on_class.missions.filter(day__lte=now)
    else:
        missions = []
    submitted = set()
    for mission in missions:
        submission = MissionSubmission.objects.filter(mission=mission, person=person).first()
        if submission is not None:
            submitted.add(f"{mission}")
    return render(request, template_name="missions/list.html", context={
        "missions": missions,
        "person": person,
        "submitted": submitted
    })
