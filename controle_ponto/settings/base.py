"""Configurações gerais do projeto controle_ponto."""

import environ
from django.conf import global_settings
from django.core import urlresolvers

root = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env()


# ADMINS = 'Fulano de tal=fulano@email.com,Beltrano=beltrano@email.com'
admins = env.dict('ADMINS')
ADMINS = admins.items()
MANAGERS = env.dict('MANAGERS', default=admins).items()

# Build paths inside the project like this: join(BASE_DIR, ...)
BASE_DIR = root()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {'default': env.db()}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Email
# https://docs.djangoproject.com/en/dev/topics/email/
env.EMAIL_SCHEMES.update(postoffice='post_office.EmailBackend')
vars().update(env.email_url())

DEFAULT_CHARSET = env('DEFAULT_CHARSET', default='utf-8')  # default charset in django.core.email.
# default from_email in EmailMessage.
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='webmaster@localhost')
# default prefix + subject in mail_admins/managers.
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[Django]')
# default from: header in mail_admins/managers.
SERVER_EMAIL = env('SERVER_EMAIL', default='admin@localhost')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'auditlog',
    'compat',
    'django_assets',
    'django_filters',
    'hijack',
    'hijack_admin',
    'post_office',
    'rest_framework',
    'widget_tweaks',
]

PROJECT_APPS = [
    'core.apps.CoreConfig',
    'ponto.apps.PontoConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root.path('controle_ponto')('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'controle_ponto.urls'

WSGI_APPLICATION = 'controle_ponto.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/assets/'
STATIC_ROOT = root.path('')('public')
STATICFILES_DIRS = [root.path('controle_ponto')('assets'), root.path('')('node_modules')]
STATICFILES_FINDERS = global_settings.STATICFILES_FINDERS + ['django_assets.finders.AssetsFinder']

MEDIA_URL = '/media/'
MEDIA_ROOT = root.path('')('media')

AUTH_USER_MODEL = 'core.User'
LOGIN_URL = urlresolvers.reverse_lazy('account_login')
LOGIN_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = ''
if env('DISABLE_ACCOUNT_REGISTRATION', default=False):
    ACCOUNT_ADAPTER = 'core.adapters.DisableSignupAdapter'
    REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'core.serializers.DisableSignupSerializer'
    }

OLD_PASSWORD_FIELD_ENABLED = True

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']

CACHES = {'default': env.cache_url()}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + \
    ['allauth.account.auth_backends.AuthenticationBackend']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                'rest_framework.filters.OrderingFilter')
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

HIJACK_LOGIN_REDIRECT_URL = '/'  # URI onde admins são redirecionados após logarem como um usuário
HIJACK_LOGOUT_REDIRECT_URL = '/'  # URI onde admins são redirecionados após liberarem um usuário
HIJACK_REGISTER_ADMIN = False
HIJACK_ALLOW_GET_REQUESTS = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'dev_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'ponto': {
            'handlers': ['console', 'dev_console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
