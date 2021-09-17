import json

from django.core.management import BaseCommand
from django.utils import timezone

from apps.skills.models import Skill
from apps.startups.models import Startup, Vacancy


def save_vacancies(raw_vacancy: dict):
    """Save `startup`, `vacancy` and skills to db from dict."""
    startup, _ = Startup.objects.update_or_create(
        title=raw_vacancy["startup_name"],
        defaults={
            "text": raw_vacancy["startup_description"],
            "end_date": timezone.now() + timezone.timedelta(weeks=40)
        }
    )
    vacancy, _ = Vacancy.objects.update_or_create(
        url=raw_vacancy["url"],
        defaults=dict(
            startup=startup,
            title=raw_vacancy["title"],
            description=raw_vacancy["description"],
        )
    )
    skills_objs = [
        Skill(name=skill) for skill in raw_vacancy["vacancy_skills"]
    ]
    Skill.objects.bulk_create(skills_objs, ignore_conflicts=True)
    skills = Skill.objects.filter(name__in=raw_vacancy["vacancy_skills"])
    vacancy.skills.add(*skills)


class Command(BaseCommand):
    """Represent command for grabbing results of parser in json format and
    save it to DB.
    """
    def handle(self, *args, **options):
        """Run command."""
        with open("./scraping/dump.json", "r") as file:
            vacancies_raw = json.load(file)
            for raw_vacancy in vacancies_raw:
                save_vacancies(raw_vacancy)
