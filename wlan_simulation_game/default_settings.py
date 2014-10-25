"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

from django.utils.translation import ugettext_lazy

BASE_DIR = os.path.dirname(__file__)


# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = False

# If you have problems, uncomment the next line to run the server in debug mode.
# DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'constance',
    'constance.backends.database',
    'wlan_simulation_game.game')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'wlan_simulation_game.urls'

WSGI_APPLICATION = 'wlan_simulation_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('en', ugettext_lazy('English')),
    ('de', ugettext_lazy('German')))

LOCALE_PATHS = (os.path.join(BASE_DIR, 'wlan_simulation_game', 'locale'),)

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'wlan_simulation_game', 'static'),)


# Miscellaneous

AUTH_USER_MODEL = 'game.Player'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'home'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'wlan_simulation_game', 'templates'),)


# Constance - Dynamic Django settings (django-constance)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'players_can_submit_messages': (
        False,
        ugettext_lazy('If this is active, players can submit messages to the system.')),
    'title': (
        'Some Title',
        ugettext_lazy('Title of the game. Used as first heading in the template.')),
    'subtitle': (
        'Some Subtitle',
        ugettext_lazy('Subtitle of the game. Used as second heading in the template.')),
    'headline': (
        'Some Headline',
        ugettext_lazy('Headline of the introduction text.')),
    'introduction': (
        'Introduction into WLAN Simulation Game comes here.',
        ugettext_lazy('Introduction to the game and the system.')),
    'year': (
        2014,
        ugettext_lazy('The year of the copyright note.')),
    'name': (
        'Your Name',
        ugettext_lazy('Name of the game master.')),
    'start_score': (
        20,
        ugettext_lazy('Score all players start with.')),
    'playable_cards': (
        5,
        ugettext_lazy('Maximum number of cards a player can play.')),
    'number_of_interceptions': (
        8, ugettext_lazy('Maximum number of messages a player can intercept. '
                         'Change this to 0 to disable the interception system.')),
    'ssid': (
        'My-WLAN',
        ugettext_lazy('Name of the WLAN. This is just for the access data sheet.')),
    'psk': (
        'default',
        ugettext_lazy('Password for the WLAN. This is just for the access data sheet.')),
    'url': (
        'http://192.168.0.1:8000/',
        ugettext_lazy('URL the server is listening on. This is just for the access data sheet.')),
    'hide_header_image': (
        False,
        ugettext_lazy('Hide the header image for admin users.'))}


# Template context processors

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as _TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = _TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'constance.context_processors.config')
