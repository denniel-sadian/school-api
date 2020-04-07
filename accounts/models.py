from django.db import models
from django.contrib.auth.models import User

from information.models import Department

ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher')
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=7, choices=ROLES, null=True)
    photo = models.ImageField(null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ProfileUserCreationPermission(models.Model):
    from_who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=7, choices=ROLES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, primary_key=True)
    used = models.BooleanField()
