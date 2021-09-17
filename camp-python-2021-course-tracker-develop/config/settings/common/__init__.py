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

from .crispy_forms import *

from .channels import *

# -----------------------------------------------------------------------------
# Installed Django Apps Configuration Starts Here
# -----------------------------------------------------------------------------
# REST API settings
from .drf import *

# -----------------------------------------------------------------------------
# Business Logic Custom Variables and Settings
# -----------------------------------------------------------------------------
from .business_logic import *

# -----------------------------------------------------------------------------
# CKEditor configuration
# -----------------------------------------------------------------------------
from .ckeditor import *


SITE_ID = 2
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

ADMINS = (
    ('Dmitry Semenov', 'dmitry@saritasa.com'),
    ('Roman Gorbil', 'gorbil@saritasa.com'),
)

MANAGERS = ADMINS
TESTING = False
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Custom settings
APP_LABEL = "Course Tracker"
