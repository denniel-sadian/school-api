# Generated by Django 3.0.5 on 2020-05-30 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0013_gradingsheet_has_multiple_choice_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='grading',
            field=models.CharField(choices=[('prelim', 'Prelim'), ('midterm', 'Midterm'), ('finals', 'Finals'), ('1st', 'First Grading'), ('2nd', 'Second Grading'), ('3rd', 'Third Grading'), ('4th', 'Fourth Grading')], max_length=7),
        ),
        migrations.AlterField(
            model_name='gradingsheet',
            name='grading',
            field=models.CharField(choices=[('prelim', 'Prelim'), ('midterm', 'Midterm'), ('finals', 'Finals'), ('1st', 'First Grading'), ('2nd', 'Second Grading'), ('3rd', 'Third Grading'), ('4th', 'Fourth Grading')], max_length=7),
        ),
    ]
