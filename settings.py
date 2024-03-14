# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

VERSION = "1.0.17"
APPLICATION = "Cash Manager"
MOBILE_VERSION = "1.3.2"
JQUERY_VERSION = "2.1.1"
EXT_VERSION = '2.2.1'

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

EMAIL_QUEUE_NAME='mail-queue'

TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True
TZ_OFFSET = -180

SECRET_KEY = '1234567890'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'djangotoolbox',
    'dbindexer',
    'adminplus',
    'pycash',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pycash.auth.middleware.RemoteTokenMiddleware',
    'pycash.auth.loginmiddleware.LoginRequiredMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'common.context_processors.settings',
    'common.context_processors.requestid',
    'pycash.context_processor.current_date',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

AUTHENTICATION_BACKENDS = ('pycash.auth.backends.RemoteTokenBackend',
                         'django.contrib.auth.backends.ModelBackend',)
                               
LOGIN_URL = '/login'
LOGIN_EXEMPT_URLS = '/cron' # this auth is managed by appengine
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

EXPORT_URL = 'localhost:8080/api/import/'

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

MEDIA_ROOT = os.path.join(PROJECT_PATH,'media_store')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'media')

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_URL = '/site_store/'
STATIC_URL = '/media/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'pycash', 'templates'),)

EXT_LOCATION = 'js/ext/' + EXT_VERSION + '/'
UX_LOCATION = EXT_LOCATION + 'ux/'

if on_production_server:
    EXT_FILES = ['js/jquery/jquery-' + JQUERY_VERSION + '.min.js',
                 EXT_LOCATION + 'adapter/jquery/ext-jquery-adapter.js',
                 EXT_LOCATION + 'ext-all.js']
else:
    EXT_FILES = ['js/jquery/jquery-' + JQUERY_VERSION + '.min.js',
                 EXT_LOCATION + 'adapter/jquery/ext-jquery-adapter.js',
                 EXT_LOCATION + 'ext-all-debug.js']

#JQMOBILE_URL = 'http://code.jquery.com/mobile'
JQMOBILE_URL = 'https://appmediaserver.appspot.com/media/lib/jquery.mobile'
JQURL = 'https://ajax.googleapis.com/ajax/libs/jquery'
                 
USE_GOOGLE_CAL = True
ENABLE_RECORD = True
RUN_ON_APPENGINE = False

ROOT_URLCONF = 'urls'

LANGUAGE_CODE = 'es'

EXPENSES_DEFAULT_DAYS_LIST = 5
TAX_DEFAULT_DAYS_ADVANCE = 5
INCOME_DEFAULT_DAYS_AHEAD = 150

try:
    execfile(os.path.join(PROJECT_PATH,'settings_local.py'))
except IOError:
    GOOGLE_USER = "-"
    GOOGLE_PASS = "-"
