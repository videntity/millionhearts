import os

from settings import *

DEBUG = False
TIME_ZONE = 'America/New_York'

#Database Settings ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBPATH = os.path.join(BASE_DIR, 'crypdb/db.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'p$
        'NAME': DBPATH,                         # Or path to database file if u$
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for local$
        'PORT': '',                             # Set to empty string for defau$
    }
 }


# Twilio SMS Login Settings ---------------------------------------------------
TWILIO_DEFAULT_FROM = "+12024992459"
TWILIO_API_BASE = "https://api.twilio.com/2010-04-01"
TWILIO_SID = "AC4d3f4dcee199445c45faa797c5c97898"
TWILIO_AUTH_TOKEN = "d623565a60e77bb5902e1971948c6f17"
TWILIO_API_VERSION = '2010-04-01'
SMS_LOGIN_TIMEOUT_MIN = 10

# Email Settings --------------------------------------------------------------

EMAIL_HOST_USER = 'hive@videntity.com'
HOSTNAME_URL = 'https://hive.communityeducatyiongroup.org'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAIE5XDCZ5PNK4RGOQ'
AWS_SECRET_ACCESS_KEY = '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'

STATIC_URL="https://statichive.s3.amazonaws.com/static/"
ADMIN_MEDIA_PREFIX = 'https://cegdjadmin.s3.amazonaws.com/'

# SFTP upload.
SFTP_HOST = 22
SFTP_HOST = ''
SFTP_USERNAME = ''
SFTP_PASSWORD = ''
SFTP_REMOTE_PATH = ''

#Backup settings --------------------------------------------------------------
AWS_BUCKET = "cegphi"
AWS_KEY = AWS_ACCESS_KEY_ID
AWS_SECRET = AWS_SECRET_ACCESS_KEY
AWS_PUBLIC = False
AWS_FIXTURE_BACKUP_FILENAME = 'hive-fixture-backup.des3'
AWS_BIN_BACKUP_FILENAME = 'hive-bin-backup.des3'

# force authentification for all pages
MIDDLEWARE_CLASSES += ('hive.utils.middleware.LoginRequiredMiddleware',)

# SOAP
USING_HTTPS = True
GPRA_SOAP_RTI_CALLER_ID = '132'
GPRA_SOAP_RTI_USERNAME = 'rtisoapservice'
GPRA_SOAP_RTI_PASSWORD = 'zpp1XxTk6RWBt%n3'

GPRA_SOAP_RTI_CLIENT_USERNAME = 'uSERVICESDC'
GPRA_SOAP_RTI_CLIENT_PASSWORD = 'rti1234'
GPRA_SOAP_RTI_WSDL_URL = 'https://www.samhsa-gpra.samhsa.gov/upload/uploadservice/uploaddocumentservice.asmx?WSDL'

VERIFY_SSL_CERTIFICATES = True

# Make sessions die out fast for more security --------------------------------
#logout after 10 minutes of inactivity
SESSION_COOKIE_AGE=600
#logout if the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
