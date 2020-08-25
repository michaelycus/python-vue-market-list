""" Production Settings """

import os
import django_heroku
import dj_database_url

############
# DATABASE #
############
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}


############
# SECURITY #
############

DEBUG = bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']

# Activate Django-Heroku.
django_heroku.settings(locals())
