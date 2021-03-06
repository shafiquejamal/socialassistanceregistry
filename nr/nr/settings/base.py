# Django settings for nr project.
from unipath import Path
import os
from django.core.exceptions import ImproperlyConfigured
PROJECT_DIR = Path(__file__).ancestor(3)
 
# -------------------------------- For userena ----------------------------------------
AUTHENTICATION_BACKENDS = (  
        'userena.backends.UserenaAuthenticationBackend',  
        'guardian.backends.ObjectPermissionBackend',  
        'django.contrib.auth.backends.ModelBackend',  
   )
 
ANONYMOUS_USER_ID = -1 
 
AUTH_PROFILE_MODULE = 'accounts.MyProfile'  
LOGIN_REDIRECT_URL = '/applicants/'
USERENA_SIGNIN_REDIRECT_URL = '/applicants/'
LOGIN_URL = '/accounts/signin/'  
LOGOUT_URL = '/accounts/signout/'  
USERENA_DEFAULT_PRIVACY = 'closed'
USERENA_HIDE_EMAIL = True
USERENA_ACTIVATION_REQUIRED = True
USERENA_SIGNIN_AFTER_SIGNUP = False
USERENA_REDIRECT_ON_SIGNOUT = "/"
 
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n'
    )
 
# -------------------------------- end For userena ------------------------------------
  
APPLICANTS_EXTRA_HOUSEHOLDMEMBER_FIELD = 10

 
DEFAULT_FROM_EMAIL = 'admin@socialassistanceregistry.com'
 
def get_env_variable(var_name):
    ''' Get the environment variable or return exception '''
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the %s environment variable' % var_name
        raise ImproperlyConfigured(error_msg)
 
MASKING_KEY = int(get_env_variable('MASKING_KEY'),16)
INLINEFORMSET_MAXNUM = 200

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}


DATABASES['default']['ENGINE']   = get_env_variable('databases_default_engine')
DATABASES['default']['NAME']     = get_env_variable('databases_default_name')
DATABASES['default']['USER']     = get_env_variable('databases_default_user')
DATABASES['default']['PASSWORD'] = get_env_variable('databases_default_password')
DATABASES['default']['HOST']     = get_env_variable('databases_default_host')
DATABASES['default']['PORT']     = get_env_variable('databases_default_port')
EMAIL_HOST = get_env_variable('email_host')
EMAIL_HOST_USER = get_env_variable('email_host_user')
EMAIL_HOST_PASSWORD = get_env_variable('email_host_password')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
#USE_L10N = False
#DATE_FORMAT = "m/d/Y"

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_DIR.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_DIR.child('static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_DIR.child('static_localstaticfiles'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nr.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'nr.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    'templatetagsapp',
    'reversion',
# -------------------------------- For userena ------------------------------------
    'userena',
    'guardian',
    'easy_thumbnails',
    'accounts',
    'applicants',
    'widget_tweaks',
    'mathfilters',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
