from django.core.management import call_command

from ..management.commands.fill_sample_data import Command
from ..models import Startup, Vacancy


def test_fill_data_command_creates_startups():
    """Test `fill_data_samples` command creates startup instances."""
    startups_before = Startup.objects.count()
    call_command('fill_sample_data')
    startups = Startup.objects.count()
    assert startups_before + Command.startups == startups


def test_fill_data_command_creates_vacancies():
    """Test `fill_data_samples` command creates vacancy instances."""
    vacancies_before = Vacancy.objects.count()
    call_command('fill_sample_data')
    vacancies = Vacancy.objects.count()
    expected_amount = (vacancies_before + Command.vacancies) * Command.startups
    assert expected_amount == vacancies
