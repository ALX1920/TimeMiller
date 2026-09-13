# TimeMiller — Backend del contador de visitas (pendiente, para el futuro)

> **Nota:** ahora mismo NO estoy usando este backend. El contador de
> visitas de TimeMiller lo resuelvo con un badge externo (hitscounter.dev),
> sin servidor propio — ver el `<img>` en `index.html`. Dejo este backend
> armado, probado y documentado por si algún día quiero mis propias
> estadísticas de visitas sin depender de un tercero. Mientras no lo
> despliegue, esta carpeta no afecta en nada al sitio.

API mínima en Django para llevar la cuenta de cuántas personas han entrado
a TimeMiller. Cuenta **visitantes únicos por día** (usando un hash de la IP,
nunca la IP en texto plano), no cada recarga de página.

## Endpoints

| Método | Ruta                    | Qué hace                                                                                      |
| ------ | ----------------------- | --------------------------------------------------------------------------------------------- | -------- |
| GET    | `/api/visits/`          | Devuelve `{"visits": N}` sin incrementar el contador.                                         |
| POST   | `/api/visits/register/` | Registra la visita (si es la primera de esa IP hoy) y devuelve `{"visits": N, "counted": true | false}`. |

## Si algún día decido activarlo

### 1. Levantarlo con Docker

```bash
cd backend
cp .env.example .env
# edito .env: DJANGO_SECRET_KEY, VISIT_SALT y CORS_ALLOWED_ORIGINS con mi dominio real

docker compose up --build -d
```

Esto deja la API escuchando en `http://localhost:8000`. En producción le pongo
delante un reverse proxy con HTTPS (Caddy, Nginx, Traefik — lo que use en mi
VPS) apuntando al puerto 8000.

### 2. Reemplazar el badge externo por mi propio backend

Ahora mismo `index.html` tiene esto:

```html
<img src="https://hitscounter.dev/api/hit?url=..." />
```

Si activo este backend, lo cambiaría por un pequeño `fetch` en `js/script.js`
que llame a `POST /api/visits/register/` al cargar la página y pinte el
número que me devuelva. Es el mismo patrón que ya usé la primera vez que
armé esto — lo dejo apuntado aquí para no tener que pensarlo de nuevo.

### 3. Crear un superusuario (para ver el total en `/admin/`)

```bash
docker compose exec web python manage.py createsuperuser
```

## Notas de seguridad (para cuando lo despliegue)

- Cambio `DJANGO_SECRET_KEY` y `VISIT_SALT` antes de desplegar — los valores
  de ejemplo son solo para desarrollo local.
- `CORS_ALLOWED_ORIGINS` debe ser el dominio exacto de mi frontend; si no
  coincide, el navegador bloquea las peticiones (error de CORS en consola,
  no un 500).
- No guardo ninguna IP en texto plano, solo un hash SHA-256 con sal.

## Desarrollo local sin Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=True
python manage.py migrate
python manage.py runserver
```
