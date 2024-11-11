from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-trqo849nebg5-%y@n^$%sva2!gs)m(e%bjdoa3j_z^(()90(r2'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chordsiteapis",
    "django_mongoengine",
    'corsheaders',
    'rest_framework',
    'django_ses',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

AWS_ACCESS_KEY_ID = 'AKIAZKYLDIPKA7NEASUJ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'chordenginev2'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
DEFAULT_FROM_EMAIL = 'brownbreadchannel@gmail.com'
EMAIL_BACKEND = 'django_ses.SESBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'chordsitebackend.urls'

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

WSGI_APPLICATION = 'chordsitebackend.wsgi.application'

MONGODB_DATABASES = {
    'default': {
        'name': 'chordsite',
        'host': 'localhost',
        'port': 27017,
        "tz_aware": True,
    },
}

# MONGODB_DATABASES = {
#     "default": {
#         "name": "Chordengine",   
#         "host": "mongodb+srv://souravmohanty0077:Vn18HDOf6cmWJn1M@cluster0.9mrj2si.mongodb.net/",
#         "tz_aware": True,                    
#     },
# }

SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
