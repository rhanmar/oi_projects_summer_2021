from datetime import timedelta

TOPIC_DAY_DELTA_CHOICES = [(i, i) for i in range(1, 6)]

# Max count days before default speaker will be set for topic.
MAX_DAYS_FOR_BECOME_MENTOR = 5

COUNT_DAYS_FOR_NOTIFICATION = timedelta(days=1)
