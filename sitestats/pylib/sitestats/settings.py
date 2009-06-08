import os
import sys
filename = __file__
package_dir = os.path.abspath(os.path.dirname(filename))
sys.path.append(package_dir + "/../../../pylib")
import mysociety.config
mysociety.config.set_file(os.path.abspath(package_dir + "/../../conf/general"))

# Django settings for sitestats project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = mysociety.config.get('SITESTATS_DB_NAME')             # Or path to database file if using sqlite3.
DATABASE_USER = mysociety.config.get('SITESTATS_DB_USER')            # Not used with sqlite3.
DATABASE_PASSWORD = mysociety.config.get('SITESTATS_DB_PASS')          # Not used with sqlite3.
DATABASE_HOST = mysociety.config.get('SITESTATS_DB_HOST')              # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = mysociety.config.get('SITESTATS_DB_PORT')              # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sy#2f70)r*6*xwwi(zqvsdmrkjdx(uxccv0qka-gi@-525s14+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sitestats.backports.contrib.auth.middleware.RemoteUserMiddleware',

)

AUTHENTICATION_BACKENDS = (

    'sitestats.backports.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',   

)


ROOT_URLCONF = 'sitestats.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'sitestats.newsletters',
    'django.contrib.admin'
)
