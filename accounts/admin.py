from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'department', 'role', 'photo')


class ProfileUserCreationInvitationAdmin(admin.ModelAdmin):
    list_display = ('date', 'role', 'first_name', 'last_name', 'department', 'from_who')


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileUserCreationInvitation, ProfileUserCreationInvitationAdmin)
