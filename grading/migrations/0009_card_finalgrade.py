# Generated by Django 3.0.5 on 2020-04-27 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('information', '0006_delete_guardianviewingpermission'),
        ('grading', '0008_auto_20200426_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grading', models.CharField(choices=[('prelim', 'Prelim'), ('midterm', 'Midterm'), ('finals', 'Finals')], max_length=7)),
                ('sem', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], max_length=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('remarks', models.CharField(default="How's this student?", max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cards', to='information.Student')),
            ],
            options={
                'unique_together': {('student', 'sem', 'grading')},
            },
        ),
        migrations.CreateModel(
            name='FinalGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=60)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_grades', to='grading.Card')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.Subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
