from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import Mission, MissionVisualization, MissionVisualizationInstance, MissionPerson, MissionSubmission, MissionClass


@admin.register(MissionVisualization)
class MVAdmin(admin.ModelAdmin):
    class MVInstanceInline(admin.TabularInline):
        model = MissionVisualizationInstance
    inlines = [
        MVInstanceInline,
    ]


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget}
    }
    filter_horizontal = ('for_class',)


@admin.register(MissionPerson)
class MissionPersonAdmin(admin.ModelAdmin):
    readonly_fields = ('total_xp_report',)
    filter_horizontal = ('on_class',)

    @admin.display(description=_("EXP"))
    def total_xp_report(self, instance):
        exp = instance.total_xp_classes()
        return format_html_join(
            mark_safe("<br>"),
            "{}: {}{}",
            ((class_.name, xp, _("XP")) for class_, xp in exp.items())
        ) or mark_safe("<span class='errors'>{}</span>".format(_("Can't get XP")))


@admin.register(MissionSubmission)
class MissionSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(MissionClass)
class MissionClassAdmin(admin.ModelAdmin):
    class MissionPersonInline(admin.StackedInline):
        model = MissionPerson.on_class.through
        extra = 1
        verbose_name = _("mission person")
        verbose_name_plural = _("mission persons")

    class MissionInline(admin.StackedInline):
        model = Mission.for_class.through
        extra = 1
        verbose_name = _("mission")
        verbose_name_plural = _("missions")

    inlines = [MissionInline, MissionPersonInline,]
