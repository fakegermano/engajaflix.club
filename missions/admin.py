from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Mission, MissionVisualization, MissionVisualizationInstance, MissionPerson, MissionSubmission


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


@admin.register(MissionPerson)
class MissionPersonAdmin(admin.ModelAdmin):
    pass


@admin.register(MissionSubmission)
class MissionSubmissionAdmin(admin.ModelAdmin):
    pass
