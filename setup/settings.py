from pathlib import Path
import os
import dj_database_url # Importante: adicione isso ao requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
# No Render, a SECRET_KEY deve vir de uma variável de ambiente
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure--d5g)bd&l^ss5n*uv!3f1)s7(wbdyvdz(&lp%jga7fopfu%z75')

# DEBUG deve ser False em produção
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Permite o domínio do Render e o localhost
ALLOWED_HOSTS = ['*'] # Em produção, substitua pelo seu link do Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oficina', # Seu app
]

# --- MIDDLEWARE (WhiteNoise inserido aqui) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essencial para o CSS no Render
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


# --- BANCO DE DADOS (Híbrido: SQLite local / PostgreSQL no Render) ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CONFIGURADOS PARA WHITENOISE) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Armazenamento otimizado do WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- ARQUIVOS DE MÍDIA (FOTOS DOS VEÍCULOS) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'