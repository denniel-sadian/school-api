from django.db import models

from accounts.models import Profile
from information.models import Student
from information.models import Subject
from information.models import Section
from information.models import Department


class GradingSheet(models.Model):
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey('auth.user', on_delete=models.PROTECT,
                                related_name='grading_sheets')
    department = models.ForeignKey(Department, on_delete=models.PROTECT,
                                   related_name='grading_sheets')
    section = models.ForeignKey(Section, on_delete=models.PROTECT,
                                related_name='grading_sheets')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                related_name='grading_sheets')
    publish = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.section} for {self.subject}'


class Work(models.Model):
    TYPES = (
        ('a', 'Activity'),
        ('q', 'Quiz'),
        ('e', 'Examination'),
        ('p', 'Performace'),
        ('c', 'Extra')
    )

    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    gsheet = models.ForeignKey(GradingSheet, on_delete=models.PROTECT,
                               related_name='works')
    work_type = models.CharField(max_length=1, choices=TYPES)
    highest_score = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Record(models.Model):
    date = models.DateField(auto_now_add=True)
    gsheet = models.ForeignKey(GradingSheet, on_delete=models.PROTECT,
                               related_name='records')
    student = models.ForeignKey(Student, on_delete=models.PROTECT,
                                related_name='records')
    work = models.ForeignKey(Work, on_delete=models.PROTECT, related_name='records')
    score = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.student}'s {self.work.name} for {self.gsheet.subject}"
