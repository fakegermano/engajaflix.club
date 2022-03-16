from django.db import models
from engajaflix.settings import AUTH_USER_MODEL
from datetime import date
from django.utils.translation import gettext_lazy as _


class Mission(models.Model):
    day = models.DateField(_("day"))
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    title = models.CharField(_("title"), max_length=256)
    description = models.TextField(_("description"), default="")
    attachment = models.FileField(_("attachment"), upload_to="media/missions/content/", blank=True, null=True)

    def __str__(self):
        return f"{self.day} - {self.title}"

    @staticmethod
    def earliest():
        return Mission.objects.order_by("day").first()

    def number(self):
        return (self.day - self.earliest().day).days


class MissionSubmission(models.Model):
    person = models.ForeignKey('MissionPerson', on_delete=models.CASCADE, related_name="mission_submissions")
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=256)
    email = models.EmailField(_("email"))
    description = models.TextField(_("description"), blank=True, default="")
    attachment = models.FileField(_("attachment"), upload_to="media/missions/submissions/", blank=True, null=True)

    def __str__(self):
        return f"{self.mission.day} - {self.person.who}"


class MissionPerson(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(_("uid"))

    @property
    def has_sent(self):
        today = date.today()
        if self.mission_submissions.filter(mission__day__contains=today).count() > 0:
            return True
        return False

    @property
    def who(self):
        return f"{self.user}" if self.user is not None else f"{self.uid}"

    def __str__(self):
        return f"{self.uid}" + "" if self.user is None else f" - {self.user}"


class MissionVisualization(models.Model):
    person = models.ForeignKey(MissionPerson, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)

    @property
    def view_count(self):
        return self.views.count()

    def __str__(self):
        return f"{self.person.who} saw {self.mission.day} {self.view_count} times"


class MissionVisualizationInstance(models.Model):
    visualization = models.ForeignKey(MissionVisualization, on_delete=models.CASCADE, related_name="views")
    seen_at = models.DateTimeField(_("seen_at"), editable=False)

    def __str__(self):
        return f"{self.visualization.person.who} saw {self.visualization.mission.day} at {self.seen_at}"
