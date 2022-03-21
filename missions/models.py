from django.db import models
from engajaflix.settings import AUTH_USER_MODEL, TIME_ZONE
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import pytz


class Mission(models.Model):
    day = models.DateField(_("day"))
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    title = models.CharField(_("title"), max_length=256)
    description = models.TextField(_("description"), default="")
    attachment = models.FileField(_("attachment"), upload_to="media/missions/content/", blank=True, null=True)

    class Meta:
        verbose_name = _("mission")
        verbose_name_plural = _("missions")

    def __str__(self):
        return f"{self.day} - {self.title}"

    @staticmethod
    def earliest():
        return Mission.objects.order_by("day").first()

    @property
    def number(self):
        return (self.day - self.earliest().day).days + 1


class MissionSubmission(models.Model):
    person = models.ForeignKey('MissionPerson', on_delete=models.CASCADE, related_name="mission_submissions")
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=256)
    email = models.EmailField(_("email"))
    description = models.TextField(_("description"), blank=True, default="")
    attachment = models.FileField(_("attachment"), upload_to="media/missions/submissions/", blank=True, null=True)

    class Meta:
        verbose_name = _("mission submission")
        verbose_name_plural = _("mission submissions")

    def __str__(self):
        return f"{self.mission.day} - {self.person.who}"


class MissionPerson(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(_("uid"))

    class Meta:
        verbose_name = _("mission person")
        verbose_name_plural = _("mission persons")

    @property
    def has_sent(self):
        today = datetime.now(pytz.timezone(TIME_ZONE)).date()
        if self.mission_submissions.filter(mission__day__contains=today).count() > 0:
            return True
        return False

    @property
    def who(self):
        if self.user is not None:
            return f"{self.user}"
        return f"{self.uid}"

    def __str__(self):
        if self.user is None:
            return f"{self.uid}"
        return f"{self.uid} - {self.user}"


class MissionVisualization(models.Model):
    person = models.ForeignKey(MissionPerson, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("mission visualizatiom")
        verbose_name_plural = _("mission visualizations")

    @property
    def view_count(self):
        return self.views.count()

    def __str__(self):
        return f"{self.person.who} saw {self.mission.day} {self.view_count} times"


class MissionVisualizationInstance(models.Model):
    visualization = models.ForeignKey(MissionVisualization, on_delete=models.CASCADE, related_name="views")
    seen_at = models.DateTimeField(_("seen_at"), editable=False)

    class Meta:
        verbose_name = _("mission visualization instance")
        verbose_name_plural = _("mission visualization instances")

    def __str__(self):
        return f"{self.visualization.person.who} saw {self.visualization.mission.day} at {self.seen_at}"
