# Datos Públicos — Hero del inicio y tabla paginada (UI)

Fecha: 2026-08-28

## Propósito

1. Mejorar el **espaciado del hero** en `www/index.html` (jerarquía visual, aire entre título/párrafo y CTAs).
2. **Paginación de la tabla** "Procesos/Contratos" en `www/municipalidad.html` a **máximo 10 filas**, con controles Anterior/Siguiente e indicador de rango, respetando filtros activos.

## Diseño aprobado

### Hero (index.html)
- `.hero` padding: `6rem 1.5rem 5rem` (equilibrado).
- `h1` margin-bottom: `1rem`.
- `.lead` margin-bottom: `2.75rem`.
- CTAs: padding `.8rem 1.6rem`, gap `1rem`.

### Tabla paginada (municipalidad.html + municipalidad.js)
- Máximo 10 filas por página; controles **Anterior / Siguiente** + *"Mostrando X–Y de N"*.
- Paginación respeta filtro (búsqueda + categoría); se resetea a pág. 1 al cambiar año.
- Componente simple en JS (índice + slice), sin librerías.

## Archivos

- `www/index.html` — CSS del hero.
- `www/municipalidad.html` — contenedor de paginación (`#paginacion`).
- `www/js/municipalidad.js` — estado de página, recorte, render de controles.

## Criterios de éxito

- Hero con mayor aire y jerarquía clara.
- Tabla muestra máx. 10 filas + controles; navegación funciona; filtro aplica dentro de la página activa; año resetea paginación.
- Tests OK; desplegado.