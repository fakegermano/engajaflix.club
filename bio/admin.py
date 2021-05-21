from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from bio.models import CustomUser, SocialLink


class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    can_delete = True


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Extra'), {'fields': ('description', 'phone', 'picture', 'type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Extra'), {'fields': ('description', 'phone', 'picture', 'type')}),
    )
    inlines = (SocialLinkInline,)


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
