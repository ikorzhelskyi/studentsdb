"""
Django settings for studentsdb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf import global_settings

from .env_settings import SECRET_KEY, DEBUG, TEMPLATE_DEBUG, ALLOWED_HOSTS
from .env_settings import SOCIAL_AUTH_FACEBOOK_SECRET, SOCIAL_AUTH_FACEBOOK_KEY
from .env_settings import DATABASES, STATIC_URL, MEDIA_URL, MEDIA_ROOT
from .env_settings import ADMIN_EMAIL, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_SSL
from .env_settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
#from .env_settings import PORTAL_URL

# in dev envrironment we may not have STATIC_ROOT defined
try:
    from .env_settings import STATIC_ROOT
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# directory to put html files with tests coverage report
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'coverage')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

REGISTRATION_OPEN = True
LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'
LOGIN_REDIRECT_URL = 'home'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'registration',
    'social.apps.django_app.default',
    'django_coverage',
    'students',
    'stud_auth',
    'django_jenkins',
)

MIDDLEWARE_CLASSES = (
    'studentsdb.middleware.RequestTimeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# enalbe Django i18n framework
USE_I18N = True

# default language
LANGUAGE_CODE = 'uk'

# enable Django localization
USE_L10N = True

# use zone-aware date objects
USE_TZ = True

# default timezone
TIME_ZONE = 'UTC'

TEMPLATE_CONTEXT_PROCESSORS = \
    global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "studentsdb.context_processors.students_proc",
    "students.context_processors.groups_processor",
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

# for 'registration' app
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_FORM = 'stud_auth.forms.CustomRegForm'

# add project templates directory as Django does not
# pick it default
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'students', 'templates', 'students'),
    os.path.join(BASE_DIR, 'stud_auth', 'templates'),
)

JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 'django_jenkins.tasks.run_pyflakes',)

LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'students.views.contact_admin': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}