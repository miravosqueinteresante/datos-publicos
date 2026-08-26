# Datos Públicos — FASE 6 mínima: Navegación multi-sección + rediseño 2026

Fecha: 2026-08-26

## Propósito

Iniciar la FASE 6 (plataforma pública) con un avance honesto y profesional: convertir `www/` de una página única a una **navegación multi-sección** con las secciones que tienen datos reales, y rediseñar la interfaz con un sistema visual moderno (2026). Sin secciones vacías ni contenido inventado.

## Sistema visual (decidido)

- **Claridad sobre oscuridad:** fondos claros (`#f8fafc`), tarjetas blancas, sombras suaves, radios 12px.
- **Acentos vivos:** primario indigo/violeta `#4f46e5`; secundario esmeralda `#10b981` para éxito/estado.
- **Tipografía:** stack de sistema con fallback a Inter; números tabulares para datos (`font-variant-numeric`).
- **Métricas:** tarjetas con números grandes y etiquetas.
- **Navegación:** menú sticky superior, separación clara de secciones.
- **Reutilización:** un único CSS compartido entre `www/` y `lab/`.

## Navegación multi-sección (www/)

```
www/
├── index.html        # Portada + Explorar (métricas + tabla actual mejoradas)
├── datos.html        # "Datos" — catálogo del dataset
├── metodologia.html  # "Metodología" — fuentes, proceso, limitaciones
└── css/style.css     # sistema visual compartido
└── js/app.js         # lógica de tabla/filtros (sin cambios)
└── datos/contrataciones-2026.json
```

- Menú: **Explorar · Datos · Metodología** + indicador "Próximamente: Mapas · Obras · Presupuesto · Indicadores" (visión, sin páginas vacías).
- **Explorar** (`index.html`): la página de contrataciones actual, rediseñada (métricas + tabla + filtros, sin cambios de lógica).
- **Datos** (`datos.html`): catálogo del dataset — descripción, métricas, enlace al CSV/JSON fuente en el repo, licencia.
- **Metodología** (`metodologia.html`): sección de metodología actual ampliada — fuente (DNCP, CC BY 4.0), pipeline, limitaciones, verificación oficial, trazabilidad.

## Conservar (sin cambios)

- `www/js/app.js` — lógica de tabla/filtros/búsqueda.
- `scripts/generar_datos_web.py` y `scripts/dncp_contrataciones.py` — generadores.
- `www/datos/contrataciones-2026.json` — datos web.
- `lab/index.html` — su HTML (se beneficia del CSS compartido rediseñado; revisar que siga coherente tras el rediseño).

## Criterios de éxito

- Las 3 páginas del www abren sin errores de consola y comparten el menú de navegación.
- Rediseño aplicado: CSS nuevo compartido, sin contradicciones con el HTML existente.
- La lógica de tabla/filtros sigue funcional (métricas y filtros correctos).
- `lab/` se ve coherente con el nuevo diseño.
- Sin secciones vacías ni placeholders de contenido fingido.
- Tests existentes pasan; sin romper el pipeline/generadores.
- Todo versionado y pusheado.