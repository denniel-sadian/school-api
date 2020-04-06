from django.db import models
from django.contrib.auth.models import User

from information.models import Department

ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher')
    )


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=7, choices=ROLES)
    photo = models.ImageField()


class EmployeeUserCreationInvitation(models.Model):
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=7, choices=ROLES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
