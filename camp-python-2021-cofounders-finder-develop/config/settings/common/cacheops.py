ONE_HOUR = 60 * 60

CACHEOPS = {
    "skills.Skill": {"ops": "all", "timeout": ONE_HOUR * 24},
    "users.CV": {"ops": (), "timeout": ONE_HOUR},
    "startups.Vacancy": {"ops": (), "timeout": ONE_HOUR},
    "startups.Startup": {"ops": (), "timeout": ONE_HOUR},
}
