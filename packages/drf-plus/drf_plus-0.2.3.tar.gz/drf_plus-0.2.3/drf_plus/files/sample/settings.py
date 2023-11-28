import json
import os
import sys
from pathlib import Path

from base.aws import AWSManager
from base.enums import ServerEnvironment
from dotenv import load_dotenv

# 파이썬 버전 고정
if sys.version_info.major != 3 or sys.version_info.minor != 11:
    raise RuntimeError("파이썬 버전이 올바르지 않습니다")

# .env 파일 경로 설정
load_dotenv(verbose=True)

# 서버 환경 설정
# 종류 : local, develop, staging, production
SERVER_ENVIRONMENT = os.environ.get("SERVER_ENVIRONMENT", ServerEnvironment.LOCAL)
PROJECT_NAME = os.environ.get("PROJECT_NAME", "sample")

# AWS SSM Parameter Store 조회
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_MANAGER = AWSManager(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# .env 파일이 없으면 실행
if SERVER_ENVIRONMENT != ServerEnvironment.LOCAL and os.path.isfile(".env") is False:
    AWS_MANAGER.load_parameters(f"{PROJECT_NAME}/{SERVER_ENVIRONMENT}/params")

BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_SECRET = AWS_MANAGER.get_secret(f"{PROJECT_NAME}/{SERVER_ENVIRONMENT}/settings")
DJANGO_SECRET = (
    DJANGO_SECRET if DJANGO_SECRET else json.loads(os.environ.get("DJANGO_SECRET"))
)
SECRET_KEY = DJANGO_SECRET.get("secret-key")
if SECRET_KEY is None:
    raise RuntimeError("환경 변수가 설정되지 않았습니다. .env.sample 파일을 참고해주세요")
DEBUG = os.environ.get("DEBUG", "False") in ["True", "true"]
TEST = "test" in sys.argv

# 허용 호스트
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 기본 설치 앱
INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # auth
    "allauth",
    "allauth.account",
    # drf
    "rest_framework",
    "corsheaders",
    # swagger
    "drf_spectacular",
    # debug
    "debug_toolbar",
    "django_filters",
    "drf_plus",
]

# 내부 앱
MY_APPS = [
    "app.users.apps.UsersConfig",
    "app.products.apps.ProductsConfig",
    "app.wish_drawers.apps.WishDrawersConfig",
]

INSTALLED_APPS += MY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "conf.wsgi.application"

DATABASES = {
    "default": {
        # Postgres
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": DJANGO_SECRET.get("db-user"),
        "PASSWORD": DJANGO_SECRET.get("db-password"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
    if SERVER_ENVIRONMENT != ServerEnvironment.LOCAL
    else {
        # Sqlite3
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# 데이터 베이스 검사
if SERVER_ENVIRONMENT != ServerEnvironment.LOCAL and (
    DATABASES["default"]["USER"] is None or DATABASES["default"]["PASSWORD"] is None
):
    raise RuntimeError("데이터베이스 설정이 올바르지 않습니다")

DATABASE_ROUTERS = ["conf.routers.DefaultRouter"]

# 캐시 설정
CACHES = {
    "default": {
        "BACKEND": "conf.caches.LocMemCacheBackend",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# DRF 설정
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "conf.openapi.CustomAutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "EXCEPTION_HANDLER": "base.exceptions.exception_handler",
    "NON_FIELD_ERRORS_KEY": "non_field",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_THROTTLE_RATES": {"sample_scope": "1/sec"}
    if not TEST
    else {"sample_scope": "1000/sec"},
}

# Auth 별 사이트 ID
SITE_ID = 1

# 사용자
AUTH_USER_MODEL = "users.User"

# 로그인 페이지 URL
LOGIN_URL = "/v1/accounts/login/"
# 로그인 후 이동할 URL
LOGIN_REDIRECT_URL = "/v1/accounts/profile/me/"
# 인증 BackEnd 클래스
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# 별도 승인 없이 바로 로그아웃
ACCOUNT_LOGOUT_ON_GET = True
# 인증 기본 프로토콜
ACCOUNT_DEFAULT_HTTP_PROTOCOL = os.environ.get("ACCOUNT_DEFAULT_HTTP_PROTOCOL", "http")
# email 을 기본 필드로
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = False
# 이메일 인증 필요 없음
ACCOUNT_EMAIL_VERIFICATION = "none"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# 이메일 승인 후 이동
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/"
# 이메일 발송 정보
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# OAuth2
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "SCOPES": {
        "read": "읽기 전용",
        "write": "쓰기 가능",
    },
    # 권한
    "SCOPES_BACKEND_CLASS": "conf.scopes.OAuth2Scopes",
    # 로그인 후 스콥 승인 페이지 표시 하지 않음
    "REQUEST_APPROVAL_PROMPT": "auto",
    # Authorization Code 만료 시간
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 60,
    # JWT 최대 시간
    "OIDC_JWKS_MAX_AGE_SECONDS": 3600,
    # OIDC issue 정보
    "OIDC_ISS_ENDPOINT": f"{ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{SITE_DOMAIN}",
}
# OAuth2.0 앱
OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth2_provider.Application"

# 내부 API 호출 시 사용할 도메인
ALLOWED_INTERNAL_IPS = ["127.0.0.1", "192.168.0.1"]
ALLOWED_INTERNAL_HOSTS = ["127.0.0.1:8000", "192.168.0.1:8000", "localhost:8000"]

# Celery 설정
BROKER_URL = os.environ.get("BROKER_URL")

# 센트리 설정
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if (
    SERVER_ENVIRONMENT
    in [
        ServerEnvironment.DEVELOP,
        ServerEnvironment.STAGING,
        ServerEnvironment.PRODUCTION,
    ]
    and SENTRY_DSN
):
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()], send_default_pii=True)

# MONGO 설정
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "admin")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "password")
MONGO_DB = os.environ.get("MONGO_DB", "mongo")
MONGO_DNS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

# CORS 전체 허용
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# 암호화 필드키 설정
ENCRYPTION_KEY_1 = DJANGO_SECRET.get("field-encryption-key-1")
FIELD_ENCRYPTION_KEYS = [
    ENCRYPTION_KEY_1,
]

# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": f"{PROJECT_NAME} API",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/v[0-9]",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SORT_OPERATIONS": False,
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 0,
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "agate",
        "showExtensions": True,
        "filter": True,
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "PREPROCESSING_HOOKS": ["conf.spectacular_hooks.api_ordering"],
    "POSTPROCESSING_HOOKS": [],
    "COMPONENT_SPLIT_REQUEST": True,
}

# 로깅
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }


INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
