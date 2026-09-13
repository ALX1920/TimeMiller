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
- Contador de visitantes activo por defecto (badge externo, sin backend propio)
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
├── backend/                       # backend del contador — pendiente, no en uso (ver Nota en su README)
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

## Cómo funciona el contador de visitas

Uso un badge externo (hitscounter.dev) que se actualiza solo cada vez que
alguien carga la página — no necesito servidor propio ni JavaScript extra
para esto. Está activo por defecto, apuntando a mi dominio
(`timemiller.gargantua.interestelar.alejandromtz.dev`).

Cuenta cargas de página, no personas únicas — si algún día quiero un conteo
más preciso de visitantes únicos y control total de mis datos, ya tengo un
backend en Django armado y documentado en [`backend/README.md`](backend/README.md)
(no lo estoy usando por ahora, queda ahí para el futuro).

## Desarrollo local

Es un sitio estático: basta con abrir `index.html` en el navegador, o servirlo
con cualquier servidor simple:

```bash
python3 -m http.server 8000
```

## Licencia

Uso personal y educativo. Proyecto de fans, sin afiliación con Warner Bros.
ni con la producción de _Interstellar_.
