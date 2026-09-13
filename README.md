# ⏳ TimeMiller

Un reloj en vivo inspirado en la dilatación temporal del planeta de Miller en
_Interstellar_.

TimeMiller calcula el tiempo exacto transcurrido en la Tierra desde el
**7 de noviembre de 2014 – 00:00** (fecha de estreno de la película) y lo
convierte en el tiempo equivalente en **el planeta de Miller**, usando la
proporción canónica:

**1 hora en Miller = 7 años en la Tierra**

La página se actualiza cada segundo y no requiere mantenimiento.

## Características

- Reloj en vivo del tiempo terrestre (años, meses, días, horas, min, seg)
- Reloj en vivo del tiempo equivalente en Miller
- Actualización automática, sin recargar
- Panel tipo HUD/telemetría de nave para mostrar los tiempos
- Contador de visitantes únicos por día (opcional, requiere el backend)
- Diseño 100% original, sin imágenes ni audio oficiales de la película

## Estructura del proyecto

```
timemiller/
├── index.html
├── js/
│   └── script.js
├── styles/
│   ├── main.css                 # conecta todos los componentes
│   └── components/
│       ├── reset.css
│       ├── layout.css
│       ├── header.css
│       ├── secciones.css
│       ├── reloj.css
│       ├── footer.css
│       └── utilidades.css
├── img/
│   └── gargantua.png
├── backend/                      # API opcional del contador de visitas
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── README.md                 # instrucciones de despliegue
│   ├── timemiller_backend/       # settings del proyecto Django
│   └── visits/                   # app: modelo, vistas y endpoints
└── documentation/
```

## Cómo activar el contador de visitas

El sitio funciona igual sin backend (el contador simplemente no se muestra).
Si quieres activarlo:

1. Despliega el backend — instrucciones completas en
   [`backend/README.md`](backend/README.md) (Docker + Django, listo para
   correr con `docker compose up --build -d`).
2. En `js/script.js`, pon la URL pública de tu backend en
   `VISITS_API_BASE`.

El contador cuenta **personas únicas por día** (por IP anonimizada con hash),
no cada recarga de página.

## Desarrollo local

Es un sitio estático: basta con abrir `index.html` en el navegador, o servirlo
con cualquier servidor simple:

```bash
python3 -m http.server 8000
```

## Licencia

Uso personal y educativo. Proyecto de fans, sin afiliación con Warner Bros.
ni con la producción de _Interstellar_.
