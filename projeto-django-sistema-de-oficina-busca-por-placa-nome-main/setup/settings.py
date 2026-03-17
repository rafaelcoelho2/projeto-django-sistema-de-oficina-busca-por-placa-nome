from pathlib import Path
import os

# Tenta importar o dj_database_url para o Postgres (Railway/Render)
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure--d5g)bd&l^ss5n*uv!3f1)s7(wbdyvdz(&lp%jga7fopfu%z75')

# Em produção, DEBUG deve ser False. No PC, o padrão é True.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# --- CONFIGURAÇÃO CSRF (CORREÇÃO PARA O RAILWAY) ---
RAILWAY_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN') or os.environ.get('RAILWAY_STATIC_URL')

CSRF_TRUSTED_ORIGINS = [
    'https://projeto-django-sistema-de-oficina-busca-por-plac-production.up.railway.app',
    'https://*.up.railway.app',
]

if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_DOMAIN}")

# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oficina', 
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise deve vir logo após o SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

# --- BANCO DE DADOS (HÍBRIDO) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Ajuste: Só tenta configurar se houver a variável e a biblioteca estiver instalada
db_from_env = os.environ.get('DATABASE_URL')
if dj_database_url and db_from_env:
    DATABASES['default'] = dj_database_url.config(
        default=db_from_env,
        conn_max_age=600,
        ssl_require=True if not DEBUG else False
    )

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- ARQUIVOS DE MÍDIA ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'