"""
Django settings for Search_Rescue project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

import mongoengine
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将当前路径加入到系统索引中
sys.path.insert(0, BASE_DIR)
# 将所有的app统一放在apps文件夹中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e0$su0(h!1%_be7%j6@7l&v6*)$&p))lcig15e*9#_^gza4i(#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    # 引入drf的token
    'rest_framework.authtoken',
    'corsheaders',
    'rescue',
    'oilspilling',
    # django.core.exceptions.ImproperlyConfigured: Application labels aren't unique, duplicates: user
    # 'user',
    'users',
    # TODO:[-] 20-02-15 加入了数据字典app
    'common',
    'geo',
    'rela',
    # 'apps.user',
    # 'common'
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Search_Rescue.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Search_Rescue.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'searchrescue',  # 数据库名
        # by casablanca
        # mac
        'USER': 'root',  # 账号
        # 7530,mac
        'PASSWORD': 'admin123',
        # 5820
        # p52s
        # 'PASSWORD': '123456',
        # by cwb
        # 'USER': 'root',  # 账号
        # 'PASSWORD': '123456',
        'HOST': '127.0.0.1',  # HOST
        'POST': 3306,  # 端口
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    }

}

# TODO:[-] 20-01-08 为了使用jwt而引入的
REST_FRAMEWORK = {
    # 加入了分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 200,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 引入第三方的jwt认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# TODO:[-] 20-01-08 加入jwt的设置（主要是过期时间）
JWT_AUTH = {
    # TODO:[-] 20-02-13 不再加入token的过期时间，配合前端 验证(暂时不加入过期时间)
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=24 * 60 * 60)
}
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 使用mongoengine
# TODO [*] 此处暂时注释掉，不然会报错，稍后解决
# SESSION_ENGINE = 'mongoengine.django.sessions'
_MONGODB_USER = 'mongouser'
_MONGODB_PASSWD = 'password'
_MONGODB_HOST = 'thehost'
_MONGODB_NAME = 'searchrescue'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)

mongoengine.connect(_MONGODB_NAME)

# TODO:[*] 19-12-29 加入了celery执行耗时的任务

# celery settings
# celery中间人 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://localhost:6379/0'
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE

# nc文件存储的根目录
NC_STORE_DIR = r''

# TODO:[-] 20-01-22 加入了分页的部分配置
PAGINATION = {
    'DEFAULT_COUNT': 500,
    'DEFAULT_INDEX': 0
}

# 测试时使用的读取nc文件的路径
NC_OPTIONS = {
    # 7530
    '_ROOT_DIR': r'D:\02proj\SearchRescue\SearchRescueSys\data\demo_data',
    # 5820
    # _ROOT_DIR = r'D:\02proj\new_SearchRescueSys\SearchRescueSys\data\demo_data'
    # 5510
    # _ROOT_DIR = r'C:\01Proj\SearchRescueSys\data\demo_data'
    # p52s
    # _ROOT_DIR = r'D:\03data\oil',
    '_RESULT_FILE': 'sanjioil.nc'
}
# 7530
# _ROOT_DIR = r'D:\03data\search'
_ROOT_DIR = r'/Users/evaseemefly/Documents/03Data/nc'
# 5820
# _ROOT_DIR = r'D:\02proj\new_SearchRescueSys\SearchRescueSys\data\demo_data'
# 5510
# _ROOT_DIR = r'C:\01Proj\SearchRescueSys\data\demo_data'
# p52s
# _ROOT_DIR = r'D:\03data\oil'

_RESULT_FILE = 'sanjioil.nc'
