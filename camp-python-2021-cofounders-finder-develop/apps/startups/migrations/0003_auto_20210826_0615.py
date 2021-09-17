# Generated by Django 3.2.5 on 2021-08-26 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('startups', '0002_startup_update_status_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='url',
            field=models.URLField(blank=True, help_text='Can be set if vacancy aggregated from other service.', null=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='owner',
            field=models.ForeignKey(blank=True, help_text="Startup's owner. Can be NULL if aggregated from other service.", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='startups', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]