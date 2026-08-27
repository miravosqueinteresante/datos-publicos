# Nota técnica — Hesakã: PDFs con texto no extraíble (brecha verificada)

Fecha: 2026-08-27
Contexto: intento de construir el pipeline de personal (salarios) 2024 del módulo presupuesto.

## Hallazgo

El PDF de Hesakã (ej. `Enero_2024.pdf`, 402 páginas) **no permite extraer texto real** por vías estándar:

- `get_text()` de PyMuPDF devuelve **~8.000 caracteres por página pero 0 alfanuméricos reales** — solo bytes (0x01-0x1F) producto de un **mapa de bytes de fuente corrupto**.

- **No es un escaneado**: las páginas tienen **0 imágenes**; las fuentes están embebidas como TrueType con nombres fragmentados:
  - `EPRQUE+TimesNewRomanPSMTFID2538HGSet2`
  - `OBZVQT+ArialMTFID5HGSet2`
  - `HAIFFG+CarlitoFID35HGSet2`
  El sufijo `FID<n>HGSet2` sugiere una exportación con mapeo de fuente deficiente.

- El renderizado de páginas a imagen es posible (2.105×1.488 px a 2.5x), pero **hacer OCR requiere instalar `tesseract`** (no presente en la máquina) o un OCR pip pesado.

- Corrección de la conclusión de una investigación previa: un subagente afirmó que "Enero_2024 tenía capa de texto" por detectar operadores `BT/Tj`; **eso es falso** — los operadores existen pero el texto NO es legible (Capa Texto rota).

## Alcance del esfuerzo para recuperar

| Vía | Costo | Riesgo |
|---|---|---|
| Instalar tesseract + OCR de 402 páginas/mes × 12 meses (2024) = ~4.800 páginas | Alto (horas de OCR + limpieza) | Números erróneos en salarios |
| Reconstruir el CMap/ToUnicode del PDF en Python | Muy alto (ingeniería de bajo nivel, por PDF) | Frágil, podría fallar por PDF |
| Renderaizar + tesseract con tabla de rectángulos | Alto | Depende de tesseract instalado |

## Veredicto

Hesakã **no es un pipeline "pequeño, completo y confiable"** (criterio del plan maestro) sin una etapa previa de ingeniería de extracción. Se documenta como **brecha técnica**, igual que la nómina nacional.

## Alternativas para la capa de personal

1. **Presupuesto/ejecución 2024** (ya disponible): la partida 100 Servicios Personales (788.089 vigente / 727.234 obligado / 92% ejecución) da el **monto agregado de personal** — la fuente confiable para "cuánto gasta la Muni en personal" sin Hesakã.
2. **SFP / nómina nacional**: requiere replicar el filtro del SPA (brecha separada).
3. **Pedido de acceso a información** a la Muni por la nómina en formato abierto.

La capa de personal del ciclo 2024 **queda representada por la partida agregada** (Servicios Personales) hasta que una de las vías alternativas se desbloquee.