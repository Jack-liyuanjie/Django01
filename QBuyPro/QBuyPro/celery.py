# --coding:utf-8--
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'QBuyPro.settings')

app = Celery('QBuyPro',
             broker='redis://:123456@116.62.193.152:6379/8',
             backend='redis://:123456@116.62.193.152:6379/9',
             namespace='Calery')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
