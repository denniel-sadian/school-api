from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'department', 'role', 'photo')


class ProfileUserCreationPermissionAdmin(admin.ModelAdmin):
    list_display = ('date', 'role', 'first_name', 'last_name', 'department', 'used')


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.StudentAccountCreationPermission)
admin.site.register(models.ProfileUserCreationPermission, ProfileUserCreationPermissionAdmin)
