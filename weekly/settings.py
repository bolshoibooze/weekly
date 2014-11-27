from __future__ import absolute_import

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Arthur Mwai', 'mwaigaryan@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'news_stand',
        'USER': 'siteadmin',
        'PASSWORD': 'siteadmin_53$*',
        'HOST': 'localhost',
        'PORT': '',
    }
}




ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Africa/Nairobi'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static/media/')

FILE_UPLOAD_PERMISSIONS = 0644

MEDIA_URL = '/static/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static/')

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    #os.path.join(os.path.dirname(__file__), 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#Cache Settings
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

CACHE_MIDDLEWARE_SECONDS = 3600



#default plus additional caches
CACHES = {
  'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT':60,
    }
}

USE_ETAGS = True
DATE_INPUT_FORMATS = '%d-%m-%Y'


#secret key and the rest

SECRET_KEY = '^&c^gzeau$ltd%_hw6@t@iqvu99c6l*#+6%tn163-a3*mwsxcz'

CSRF_COOKIE_DOMAIN = None

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',   
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
   
    
)


MIDDLEWARE_CLASSES = (
    #cache
    'django.middleware.cache.UpdateCacheMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'htmlmin.middleware.MarkRequestMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.core.context_processors.csrf',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yawdadmin.middleware.PopupMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
   
)


#AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)


ROOT_URLCONF = 'weekly.urls'


WSGI_APPLICATION = 'weekly.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yawdadmin',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'fluent_comments',
    #'crispy_forms',
    'django.contrib.comments',
    
   
    'home',
    'about',
    'photos',
    'users',
    'tinymce',
    'form_utils',
    'sorl.thumbnail',
    'notifications',
    'ua_detector',
    
    #'south',
    
)

AUTH_USER_MODEL = 'users.ExtendedUser'

DEFAULT_FROM_EMAIL = 'weeklykenyan'


#POPULARITY_LISTSIZE = '30'

FLUENT_COMMENTS_EXCLUDE_FIELDS = ('name', 'email', 'url')
COMMENTS_APP = 'fluent_comments'



SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}




