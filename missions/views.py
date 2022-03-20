from django.shortcuts import render
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy
from django_user_agents.utils import get_user_agent
import pytz

from engajaflix.settings import TIME_ZONE

from .models import MissionPerson, Mission, MissionVisualization, MissionSubmission
from .forms import SubmissionForm


def index(request):
    user_agent = get_user_agent(request)
    can_share = not user_agent.is_pc and user_agent.os.family != "iOS"
    now = datetime.utcnow().replace(tzinfo=pytz.timezone(TIME_ZONE))
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
        form = SubmissionForm()
    elif request.method == "POST" and mission:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.name = request.user.first_name
            submission.email = request.user.email
            submission.person = person
            submission.mission = mission
            submission.save()
    midnight = (now + timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
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

    return render(request, template_name="missions/index.html", context={
        "mission": mission,
        "has_sent": person.has_sent,
        "next_mission": (midnight - now).seconds,
        "can_share": can_share,
        "share_text": share_text,
        "form": form,
    })
