from .health_check import HEALTH_CHECKS_APPS

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
    'crispy_forms',
)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DRF_PACKAGES = (
    'rest_framework',
    'knox',
    'drf_spectacular',
    'django_filters',
)

THIRD_PARTY = (
    'corsheaders',
    'storages',
    'imagekit',
    'django_celery_beat',
    'django_extensions',
    'watson',
    'channels',
)

LOCAL_APPS = (
    'apps.core',
    'apps.users',
    'apps.map',
    'apps.dialogs',
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + HEALTH_CHECKS_APPS + LOCAL_APPS
