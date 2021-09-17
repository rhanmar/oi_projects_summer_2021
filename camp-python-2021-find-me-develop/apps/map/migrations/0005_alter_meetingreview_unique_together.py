# Generated by Django 3.2.5 on 2021-08-18 10:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map', '0004_alter_meeting_created_by'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='meetingreview',
            unique_together={('meeting', 'created_by')},
        ),
    ]
