"""
Configuración de Django para timemiller_backend.

NOTA MÍA: este backend no está desplegado ni en uso todavía. Por ahora el
contador de visitas de TimeMiller lo resuelvo con un badge externo (ver
index.html). Dejo este backend armado y probado para el día que quiera
tener mis propias estadísticas de visitas sin depender de un tercero.

Leo todo lo sensible o dependiente del entorno desde variables de entorno
(ver .env.example) para poder correr esto en Docker sin tocar código.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


# --- Seguridad básica ---
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme-dev-secret-do-not-use-in-production")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

# Uso esta sal para anonimizar IPs antes de guardarlas (nunca guardo la IP en texto plano)
VISIT_SALT = os.environ.get("VISIT_SALT", "changeme-salt")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "visits",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "timemiller_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "timemiller_backend.wsgi.application"

# --- Base de datos ---
# Elegí SQLite porque es suficiente para un contador de visitas; la guardo
# en un volumen de Docker para que persista entre despliegues (ver docker-compose.yml).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_DB_PATH", str(BASE_DIR / "data" / "db.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-mx"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "America/Mexico_City")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CORS ---
# Mi frontend vive en otro dominio (GitHub Pages), así que tengo que
# permitirlo explícitamente. Configuro CORS_ALLOWED_ORIGINS con mi
# dominio real cuando despliegue esto en producción.
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    "https://timemiller.gargantua.interestelar.alejandromtz.dev",
)

# Si tengo DEBUG activo (desarrollo local), permito cualquier origen para
# probar más rápido.
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Por si en el futuro pongo esto detrás de un proxy (nginx/Caddy) que termina TLS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
