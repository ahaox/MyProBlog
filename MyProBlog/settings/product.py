#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2020/1/15 20:44
"""上线运行环境配置"""

from .base import *  # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyProBlog',
        'USER': 'root',
        'PASSWORD': 'MuXu2014@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': None,
    }
}