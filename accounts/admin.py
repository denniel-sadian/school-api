from django.contrib import admin

from . import models


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'department', 'role', 'photo')


class EmployeeUserCreationInvitationAdmin(admin.ModelAdmin):
    list_display = ('date', 'role', 'first_name', 'last_name', 'department', 'photo')


admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.EmployeeUserCreationInvitation, EmployeeUserCreationInvitationAdmin)
