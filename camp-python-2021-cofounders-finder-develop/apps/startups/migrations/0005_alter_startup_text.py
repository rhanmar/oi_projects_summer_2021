# Generated by Django 3.2.5 on 2021-08-26 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0004_alter_vacancy_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='text',
            field=models.TextField(blank=True, help_text='Info about startup', max_length=2048, verbose_name='Text'),
        ),
    ]
