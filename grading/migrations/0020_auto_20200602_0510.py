# Generated by Django 3.0.5 on 2020-06-02 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0019_finalgrade_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalgrade',
            name='sheet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='final_grades', to='grading.GradingSheet'),
        ),
    ]
