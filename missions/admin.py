from django.contrib import admin

from .models import Mission, MissionVisualization, MissionVisualizationInstance, MissionPerson, MissionSubmission


class MVInstanceInline(admin.TabularInline):
    model = MissionVisualizationInstance


class MVAdmin(admin.ModelAdmin):
    inlines = [
        MVInstanceInline,
    ]


admin.site.register(Mission)
admin.site.register(MissionVisualization, MVAdmin)
admin.site.register(MissionPerson)
admin.site.register(MissionSubmission)
