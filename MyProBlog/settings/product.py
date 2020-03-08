#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2020/1/15 20:44
"""上线运行环境配置"""

from .base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS = ['www.ahaoao.top']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyProBlog',
        'USER': 'root',
        'PASSWORD': 'MuXu2014@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

ADMINS = MANAGERS = (
    ('ahao', 'xuhao@stu.cdu.edu.cn'),  # 邮件地址
)

REDIS_URL = 'r-2ze40b80cc8820a4.redis.rds.aliyuncs.com:6379:1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            'PASSWORD': 'MuXu2014@@',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}


MIDDLEWARE += [
    'django.middleware.cache.UpdateCacheMiddleware'
]
