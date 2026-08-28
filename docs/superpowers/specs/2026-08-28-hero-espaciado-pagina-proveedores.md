# Datos Públicos — Espaciado hero + página "Principales Proveedores"

Fecha: 2026-08-28

## Propósito

1. Aumentar el espaciado entre el texto del hero (título + párrafo) y los botones en la raíz (`www/index.html`).
2. Crear una página nueva `www/proveedores.html` con las 10 fichas de proveedores (hoy embebidas en `www/municipalidad.html`), accesible desde el menú **Proveedores**, con enlace desde el perfil.

## Decisiones aprobadas

- Espaciado: `.hero .lead` margin-bottom de `1.4rem` → `2.5rem` (aire claro entre texto y CTAs).
- Página nueva `www/proveedores.html` con las 10 fichas desplegables (reusa `www/datos/proveedores.json`).
- JS propio `www/js/proveedores.js` (extrae la lógica de fichas de `municipalidad.js`).
- `municipalidad.html` conserva la serie + indicadores por año; reemplaza las fichas embebidas por un **enlace destaque "Ver principales proveedores →"**.
- Menú en las 5 páginas: Municipalidad · **Proveedores** · Datos · Metodología.

## Estructura

- `www/proveedores.html` (nueva).
- `www/js/proveedores.js` (nueva; lógica de fichas).
- `www/municipalidad.html` (quitar sección de fichas → enlace).
- `www/index.html` (hero: espaciado) + nav.
- `www/datos.html`, `www/metodologia.html` (nav con Proveedores).

## Criterios de éxito

- Más aire entre texto del hero y botones (visual).
- `proveedores.html` lista las 10 fichas desplegables (mismas de hoy en municipalidad).
- Menú coherente en las 5 páginas.
- Enlace del perfil lleva a la nueva página.
- Sin cambios de datos/pipeline; tests OK; desplegado.