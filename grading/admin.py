from django.contrib import admin

from . import models


class GradingSheetAdmin(admin.ModelAdmin):
    list_display = ('date', 'teacher', 'department', 'subject', 'publish')


class WorkAdmin(admin.ModelAdmin):
    list_display = ('date', 'gsheet', 'work_type', 'highest_score')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'gsheet', 'student', 'work', 'score')


admin.site.register(models.GradingSheet, GradingSheetAdmin)
admin.site.register(models.Work, WorkAdmin)
admin.site.register(models.Record)
