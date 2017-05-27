"""
Django settings for Webtool project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
EXCEL_CONFIG_PATH = os.path.join(BASE_DIR,'temp/config_table/Config')
#redmine
# LX6
REDMINE_ISSUES_URL = 'http://lx6.leihuo.netease.com/issuelist.php?page=%s&rows_num=%s'
REDMINE_QUERYISSUE_URL = 'http://lx6.leihuo.netease.com/queryissue.php?ids=%s'
# ZQJT
REDMINE_ISSUES_URL_ZQJT = 'http://t1.pm.netease.com/issuelist.php?page=%s&rows_num=%s&project=tanjunbug&tracker=%s&status=%s'
REDMINE_QUERYISSUE_URL_ZQJT = 'http://t1.pm.netease.com/queryissue.php?ids=%s'

#svn
SVN_ROOT_URL = 'https://gamehz.163.org/svn/st/Project/LX2/'
SVN_LOG_PULL_TRUNK_NAMES = ['config', 'client','other']
# SVN_SUDO = 'sudo -iu leitingqa'

#code_diff
CODE_DIFF_URL = 'http://192.168.131.233:9090/' + '/webtool/diff/diff_code?filepath_url={filepath_url}&first_version={first_version}&last_version={last_version}'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l%=e7xuidc5^s&t&qi0)@+5l63(k=wx3@jl!jp2c8(fala$0ra'
SITE_URL='/webtool/'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'apps.moc',
    'apps.diff',
    'apps.build',
    'apps.regression',
    'apps.server_log',
    'apps.svn_cmt_assign',
    'apps.conf_query',
    'apps.info_set',
    'apps.django_openid_auth',
	'apps.assign_zqjt',
    'apps.assign_test_case',
    'apps.unity_profiling',
    'apps.analysis_performance'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'webtool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'leiting',
        'USER': 'leiting',
        'PASSWORD': 'leiting_qa_163',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# openid
OPENID_CREATE_USERS = True
LOGIN_URL = '/webtool/openid/login'
OPENID_SSO_SERVER_URL = 'https://login.netease.com/openid/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'account.backend.MyBackend',
    'apps.django_openid_auth.auth.OpenIDBackend',
)

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
LOGIN_REDIRECT_URL = 'http://192.168.131.233:9090'
