# Django settings for millionhearts project.
import os
from django.utils.translation import ugettext_lazy as _
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alan Viars', 'aviars@videntity.com'),
)
SITE_ID = 1
MANAGERS = ADMINS

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )
MANAGERS = ADMINS


DBPATH=os.path.join(BASE_DIR, 'db/db.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

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

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, 'sitestatic')

AUTH_PROFILE_MODULE = 'accounts.userprofile'



AUTHENTICATION_BACKENDS = (#'django.contrib.auth.backends.ModelBackend',
                           'apps.accounts.auth.EmailBackend',
                            'apps.accounts.auth.MobilePhoneBackend',
                           'apps.accounts.auth.HTTPAuthBackend',
                           )



# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@r_sdjk6f$r9)zafk7_vkp6fy0^m2$02k59b5)4oruoh0=xsv0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'millionhearts.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'millionhearts.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'apps/main/templates'),
    
    # This should always be the last in the list because it is our
    # fallback default.
    os.path.join(BASE_DIR, 'templates'), 
)


LOCALE_PATHS = (
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'locale'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.riskassessments',
    'apps.accounts',
    'apps.pharmacy',
    'apps.intake',
    'apps.generic',
    'apps.locations',
    'apps.dashboard',
    'bootstrapform',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# --------------------------------------------------------------------------
# Custom Project Settings --------------------------------------------------
# --------------------------------------------------------------------------


# Email Settings -----------------------------------------------------------

EMAIL_HOST_USER = 'beheartsmart@videntity.com'
HOSTNAME_URL = 'https://beheartssmart.com'
#HOSTNAME_URL = 'http://127.0.0.1:8000'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAI3FSWI4AOSJKO6IA'
AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FROM_EMAIL='beheartsmart@videntity.com'
SERVER_EMAIL='beheartsmart@videntity.com'

# Twilio SMS Login Settings -----------------------------------------------
TWILIO_DEFAULT_FROM = "+14106967670"
TWILIO_API_BASE = "https://api.twilio.com/2010-04-01"
TWILIO_SID = "ACccc139f8b71ff89e90678aa10988d3dc"
TWILIO_AUTH_TOKEN = "416186fcde814074209dbb3c723432a9"
TWILIO_API_VERSION = '2010-04-01'
SMS_LOGIN_TIMEOUT_MIN = 10
SMS_REMINDER_MESSAGE = _("Reminder from BeHeartSmart.com: Get you blood pressure and cholesterol screen tomorrow.")

EMAIL_REMINDER_SUBJECT = _("Reminder from BeHeartSmart.com: Get you blood pressure and cholesterol screen tomorrow.")
EMAIL_REMINDER_BODY    = _("This is a reminder to get you blood pressure and cholesterol sceen tomorrow.  Here are the details.")



#Google MAPS API keu

GOOGLE_API_KEY = "AIzaSyATX4Joc0aP0_V0YTiIT8uvWbRbmSvBFrQ"


#Backup settings ----------------------------------------------------------
AWS_BUCKET  = "beheartsmartbackup"
AWS_KEY     = AWS_ACCESS_KEY_ID
AWS_SECRET  = AWS_SECRET_ACCESS_KEY
AWS_PUBLIC  = False
AWS_FIXTURE_BACKUP_FILENAME = 'fixture-backup.des3'
AWS_BIN_BACKUP_FILENAME = 'bin-backup.des3'

AWS_LOCAL_FIXTURE_FILEPATH = os.path.join(BASE_DIR, 'fixture-backup.des3')
AWS_LOCAL_BIN_FILEPATH = os.path.join(BASE_DIR, 'bin-backup.des3')

#Account Activation Settings -------------------------------------------------
ACCOUNT_ACTIVATION_DAYS = 2
RESTRICT_REG_DOMAIN_TO = None
MIN_PASSWORD_LEN = 5

#Org details
ORGANIZATION_NAME = "Be Heart Smart"
LOCATION_NAME = "Baltimore, MD"


# Framingham
DEFAULT_FRAMINGHAMTEST_INCENTIVE    = 10
FRAMINGHAM10YR_RETEST_DAYS          = 180

# Archimedes
ARCHIMEDES_API_URL = "https://demo-indigo4health.archimedesmodel.com/IndiGO4Health/IndiGO4Health"
SURESCRIPTS_API_URL ="https://millionhearts.surescripts.net/test/Provider/Find"
SURESCRIPTS_API_TOKEN = "3a0a572b-4f5d-47a2-9a75-819888576454"


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
