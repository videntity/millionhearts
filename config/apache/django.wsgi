import os
import sys

sys.path.append('/home/ubuntu/django-apps/millionhearts/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'millionhearts.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

