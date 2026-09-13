# TimeMiller — Backend del contador de visitas

API mínima en Django para llevar la cuenta de cuántas personas han entrado
a TimeMiller. Cuenta **visitantes únicos por día** (usando un hash de la IP,
nunca la IP en texto plano), no cada recarga de página.

## Endpoints

| Método | Ruta                     | Qué hace                                              |
|--------|--------------------------|--------------------------------------------------------|
| GET    | `/api/visits/`           | Devuelve `{"visits": N}` sin incrementar el contador.  |
| POST   | `/api/visits/register/`  | Registra la visita (si es la primera de esa IP hoy) y devuelve `{"visits": N, "counted": true|false}`. |

El frontend llama a `POST /api/visits/register/` una vez al cargar la página.

## Levantarlo con Docker (recomendado)

```bash
cd backend
cp .env.example .env
# edita .env: DJANGO_SECRET_KEY, VISIT_SALT y CORS_ALLOWED_ORIGINS con tu dominio real

docker compose up --build -d
```

Esto deja la API escuchando en `http://localhost:8000`. Detrás de eso, en
producción, pon un reverse proxy con HTTPS (Caddy, Nginx, Traefik, lo que uses
en tu VPS) apuntando al puerto 8000, y usa esa URL con HTTPS en el frontend.

## Conectarlo con el frontend

En `js/script.js`, en la raíz del proyecto, cambia:

```js
const VISITS_API_BASE = "";
```

por la URL pública de tu backend, por ejemplo:

```js
const VISITS_API_BASE = "https://api.tu-dominio.dev";
```

Si lo dejas vacío, el badge de visitas simplemente no se muestra — la página
sigue funcionando sin backend.

## Crear un superusuario (para ver el total en `/admin/`)

```bash
docker compose exec web python manage.py createsuperuser
```

## Notas de seguridad

- Cambia `DJANGO_SECRET_KEY` y `VISIT_SALT` antes de desplegar — los valores
  de ejemplo son solo para desarrollo local.
- `CORS_ALLOWED_ORIGINS` debe ser el dominio exacto del frontend; si no
  coincide, el navegador bloqueará las peticiones (verás un error de CORS
  en la consola, no un error 500).
- No se guarda ninguna IP en texto plano, solo un hash SHA-256 con sal.

## Desarrollo local sin Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=True
python manage.py migrate
python manage.py runserver
```
