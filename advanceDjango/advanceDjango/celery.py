# --coding:utf-8--
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanceDjango.settings')

app = Celery('advanceDjango',
             broker='redis://:123456@116.62.193.152:6379/8',
             backend='redis://:123456@116.62.193.152:6379/9')
app.config_from_object('django.conf:settings')  # 配置Celery，加载settings.py

app.autodiscover_tasks()  # 自动发现task任务
