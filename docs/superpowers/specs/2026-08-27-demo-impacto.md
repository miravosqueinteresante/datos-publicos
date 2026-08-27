# Datos Públicos — Página Demo de impacto (demostración política)

Fecha: 2026-08-27

## Propósito

Crear la página de entrada para la **demostración política** del proyecto: una portada impactante que cuente la historia ("con iniciativa + datos que ya existen + herramientas accesibles se construyen servicios públicos útiles") y lleve al visitante a las vistas reales (Explorar, Gasto) que ya funcionan.

Tras la evaluación estratégica independiente (objetivo = demostración política), esta página es la pieza de comunicación, no más infraestructura de datos.

## Audiencia y mensaje

**Audiencia:** el político/periodista/ciudadano que ve el proyecto por primera vez (contexto: candidatura; demostrar que la idea es real y constructible).

**Mensaje en un vistazo:**
1. **Esto es real** — Datos Públicos (enlaces a las vistas funcionando).
2. **Se construyó con datos ya públicos** — la Municipalidad y la DNCP publican; el proyecto los hace comprensibles.
3. **Qué muestra hoy** — contrataciones 2024/2026 y ejecución presupuestaria 2024 (datos reales).
4. **Qué se podría hacer** — con apoyo institucional/alianza: la frontera (visión del plan redefinida como horizonte, NO como promesa).

## Diseño

### Estructura del flujo de la demo
1. **Hero** — titular impactante + subtítulo que resume la tesis. CTA a Explorar/Gasto.
2. **"Qué es esto / por qué importa"** — 3 puntos: producto real, datos ya públicos, herramientas accesibles.
3. **Prueba viva (datos reales)** — tarjetas de métricas actuales (36 procesos 2026; 28 en 2024; ejecución 2024 ~53%; con enlaces a las páginas).
4. **"Qué encontramos y qué falta"** — honestidad estratégica: la Municipalidad no publica todo en abierto; mostramos lo que SÍ está disponible y documentamos lo que exige pedido formal (Civio-style: transparencia como fortaleza).
5. **CTA final** — ver la plataforma / el laboratorio.

### Archivos
- `www/demo.html` (o `www/index.html` rediseñada como puerta de entrada) — decido en plan: `demo.html` como landing, `index.html` sigue siendo Explorar. El deploy sirve `www/` como raíz; se puede hacer `index.html` = demo y mover explorar a `explorar.html`, o dejar demo accesible por enlace. Decisión en plan (mínima intrusión).

### Estilo
- Reutiliza `www/css/style.css` (sistema 2026 claro + acentos).
- Sin frameworks; JS vanilla solo si hace falta (métricas mínimas).

## Criterios de éxito
- Página Demo cuenta la historia en un vistazo y enlaza a las vistas reales.
- Usa datos reales (no cifras inventadas) con trazabilidad visible.
- Honesta: muestra lo disponible y lo bloqueado (sin prometer lo que no llega).
- Coherente con el diseño 2026; sin código nuevo innecesario.
- Desplegada en `datospublicos.muchotexto.net`.