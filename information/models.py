from django.db import models

class Student(models.Model):
    LEVELS = (
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
        ('c1', 'First Year College'),
        ('c2', 'Second Year College'),
        ('c3', 'Third Year College'),
        ('c4', 'Fourth Year College')
    )

    firstname = models.CharField(max_length='50')
    lastname = models.CharField(max_length='50')
    id_number = models.CharField(max_length='100')
    cp_number = models.CharField(max_length='12')
    guardian_cp_number = models.CharField(max_length='12')
    address = models.CharField(max_length='255')
    photo = models.ImageField()
    department = None
    grade_level = models.CharField(max_length='2', choices=LEVELS)
    section = None
