from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html

# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamu_be_jsvs.settings')

app = Celery('jsvs')
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)