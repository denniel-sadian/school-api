# Generated by Django 3.0.5 on 2020-04-16 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('information', '0005_auto_20200416_0832'),
        ('accounts', '0008_auto_20200416_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='information.Department'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profileusercreationpermission',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='information.Department'),
        ),
        migrations.AlterField(
            model_name='profileusercreationpermission',
            name='from_who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='permissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
