# -----------------------------------------------------------------------------
# General Django Configuration Starts Here
# -----------------------------------------------------------------------------

from .paths import *
from .security import *
from .installed_apps import *
from .authentication import *
from .internationalization import *
from .middleware import *
from .templates import *
from .static import *
from .logging import *
# storage configuration (aws s3 etc)
from .storage import *
# email and sms notifications (twilio)
from .notifications import *
# cors headers exposed
from .cors import *

from .haystack import *

from .cacheops import *

from .crispy_forms import *

# -----------------------------------------------------------------------------
# Installed Django Apps Configuration Starts Here
# -----------------------------------------------------------------------------
# REST API settings
from .drf import *

# -----------------------------------------------------------------------------
# Business Logic Custom Variables and Settings
# -----------------------------------------------------------------------------
from .business_logic import *

SITE_ID = 1
ROOT_URLCONF = 'config.urls'
# WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

ADMINS = (
    ('Dmitry Semenov', 'dmitry@saritasa.com'),
    ('Roman Gorbil', 'gorbil@saritasa.com'),
)

MANAGERS = ADMINS
TESTING = False
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Custom settings
APP_LABEL = "Cofounders Finder"
