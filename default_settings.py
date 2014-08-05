"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from django.utils.translation import ugettext_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# If you have problems, uncomment the next line to run the server in debug mode.
# DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'constance',
    'constance.backends.database',
    'wlan_simulation_game.player',
    'wlan_simulation_game.card',
    'wlan_simulation_game.message',
    'wlan_simulation_game.templatetags')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'wlan_simulation_game.urls'

WSGI_APPLICATION = 'wlan_simulation_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

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
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'wlan_simulation_game', 'static'),)


# Miscellaneous

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'wlan_simulation_game', 'templates'),)

#~ LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'home'


# Constance - Dynamic Django settings (django-constance)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'title': ('Title', ugettext_lazy('Title of the game. Used as first heading in the template.')),
    'subtitle': ('Subtitle', ugettext_lazy('Subtitle of the game. Used as second heading in the template.')),
    'headline': ('Welcome to WLAN Simulation Game', ugettext_lazy('Headline for the introduction text.')),
    'introduction': ('Introduction into WLAN Simulation Game comes here.', ugettext_lazy('Introduction to the game and the system.')),
    'year': (2013, ugettext_lazy('The year for the copyright note.')),
    'name': ('Your Name', ugettext_lazy('Name of the game master.')),
    'players_can_submit_messages': (False, ugettext_lazy('If this is active, players can submit messages to the system.')),
    'start_score': (20, ugettext_lazy('Score all players start with.')),
    'playable_cards': (5, ugettext_lazy('Maximum number of cards a player can play.')),
    'number_of_interceptions': (8, ugettext_lazy('Maximum number of messages a player can intercept.')),
    'ssid': ('WLANSimulationGame', ugettext_lazy('Name of the WLAN. This is just for the access data sheet.')),
    'psk': ('default', ugettext_lazy('Password for the WLAN. This is just for the access data sheet.')),
    'url': ('http://192.168.0.1:8000/', ugettext_lazy('URL where the server is listening on. This is just for the access data sheet.')),
    'hide_header_image': (False, ugettext_lazy('Hide the header image for administrator.'))}


# Template context processors

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as _TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = _TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'constance.context_processors.config')
