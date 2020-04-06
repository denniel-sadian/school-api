from django.db import models

from accounts.models import Employee
from information.models import Student
from information.models import Subject
from information.models import Section
from information.models import Department


class GradingSheet(models.Model):
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)


class Work(models.Model):
    TYPES = (
        ('a', 'Activity'),
        ('q', 'Quiz'),
        ('e', 'Examination'),
        ('p', 'Performace'),
        ('c', 'Extra')
    )

    date = models.DateField(auto_now_add=True)
    gsheet = models.ForeignKey(GradingSheet, on_delete=models.CASCADE, related_name='works')
    work_type = models.CharField(max_length=1, choices=TYPES)
    highest_score = models.IntegerField(default=1)


class Record(models.Model):
    date = models.DateField(auto_now_add=True)
    gsheet = models.ForeignKey(GradingSheet, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)
