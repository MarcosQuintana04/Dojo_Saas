# config/settings/production.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['marcosquintana.pythonanywhere.com']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True