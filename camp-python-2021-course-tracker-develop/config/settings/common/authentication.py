from django.urls import reverse_lazy


# Custom model for Auth

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom login redirect

LOGIN_REDIRECT_URL = reverse_lazy("homepage")

LOGIN_URL = reverse_lazy("login")

# Set URLs to be ignored by `LoginRequiredMiddleware`.

LOGIN_EXEMPT_VIEWS = [
    "admin:index",
    "admin:login",
    "signup",
    "login",
    "activate-account",
    "github_login",
    "github_callback",
    "github_webhook",
]

# Social accounts settings

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'read:org',
        ]
    }
}

# GitHub OAuth settings

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ALLOWED_GITHUB_ORGANIZATIONS = (
    "saritasa-nest",
    "malinleo-org",
    "killmoon-org",
)

ALLOWED_USER_EMAIL_DOMAINS = (
    "saritasa.com",
    "root.com",
)
