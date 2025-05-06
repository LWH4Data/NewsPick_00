from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-s@&#j#l5wou1(mxx+tc%frsjq9&z@p@f60p5%ht4mn*s8$ed6i'

DEBUG = True

ALLOWED_HOSTS = []

# 앱 설정
INSTALLED_APPS = [
    'accounts',
    'news_api',
    
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    
    'dj_rest_auth',
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'corsheaders',  # ✅ CORS 설정

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# REST 프레임워크 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SITE_ID = 1

# 미들웨어 설정
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ 반드시 가장 위에 가까이 위치
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news',
        'USER': 'ssafynews',
        'PASSWORD': 'ssafynews13',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 국제화
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 정적 파일 설정
STATIC_URL = '/static/'

# 기본 PK 필드 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 사용자 모델 설정
AUTH_USER_MODEL = 'accounts.User'

# dj-allauth 계정 설정
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username'  # ✅ 로그인 방식: username 기반
ACCOUNT_EMAIL_REQUIRED = False              # ✅ 이메일 필수 아님

# ✅ CORS 설정 추가
CORS_ALLOW_ALL_ORIGINS = True  # 개발 중엔 True로 두고, 배포 시 whitelist 방식으로 수정
