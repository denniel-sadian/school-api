# Generated by Django 3.0.5 on 2020-04-07 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='information.Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('teacher', 'Teacher')], max_length=7),
        ),
    ]
