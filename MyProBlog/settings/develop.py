#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2020/1/15 20:44
"""开发环境的配置  pycharm设置DJANGO_SETTINGS_MODULE """
from .base import *  # NOQA


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyProBlog',
        'USER': 'root',
        'PASSWORD': 'MuXu2014@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': None,  # 不限制连接时长
    }
}

# INSTALLED_APPS += [
#     # 'debug_toolbar',
#     'silk',
# ]
#
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
#     # 'silk.middleware.SilkyMiddleware',
# ]
#
# INTERNAL_IPS = ['127.0.0.1']
#
# DEBUG_TOOLBAR_PANELS = [
#     # 'debug_toolbar.panels.versions.VersionsPanel',
#     # 'debug_toolbar.panels.timer.TimerPanel',
#     # 'debug_toolbar.panels.settings.SettingsPanel',
#     # 'debug_toolbar.panels.headers.HeadersPanel',
#     # 'debug_toolbar.panels.request.RequestPanel',
#     # 'debug_toolbar.panels.sql.SQLPanel',
#     # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     # 'debug_toolbar.panels.templates.TemplatesPanel',
#     # 'debug_toolbar.panels.cache.CachePanel',
#     # 'debug_toolbar.panels.signals.SignalsPanel',
#     # 'debug_toolbar.panels.logging.LoggingPanel',
#     # 'debug_toolbar.panels.redirects.RedirectsPanel',
#
#     'djdt_flamegraph.FlamegraphPanel',
#
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
# }