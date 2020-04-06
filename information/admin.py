from django.contrib import admin

from . import models


class GuardianViewingPermissionAdmin(admin.ModelAdmin):
    list_display = ('date', 'section', 'code')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id_number', 'cp_number',
                    'guardian_cp_number', 'address', 'department', 'grade_level',
                    'section')


admin.site.register(models.Department)
admin.site.register(models.Section)
admin.site.register(models.Subject)
admin.site.register(models.GuardianViewingPermission, GuardianViewingPermissionAdmin)
admin.site.register(models.Student, StudentAdmin)
