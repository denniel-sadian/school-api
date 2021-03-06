# Generated by Django 3.0.5 on 2020-04-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_delete_guardianviewingpermission'),
        ('grading', '0006_auto_20200420_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='work_type',
            field=models.CharField(choices=[('a', 'Activity'), ('q', 'Quiz'), ('e', 'Examination'), ('p', 'Performace')], max_length=1),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('student', 'work')},
        ),
    ]
