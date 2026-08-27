# Datos Públicos — Módulo presupuesto: dataset de ejecución 2024 (Rendición de Cuentas)

Fecha: 2026-08-27

## Propósito

Construir el primer dataset del módulo presupuestario: la **ejecución del gasto 2024 de la Municipalidad de Asunción** extraída de la **Rendición de Cuentas 2024** (fuente oficial, verificada en el inventario FUENTES_2024 P05). Es el dato central disponible del ciclo: presupuesto vigente y obligado por nivel de objeto del gasto.

## Fuente

**Rendición de Cuentas 2024** — páginas 4 (tabla de ejecución) del PDF:
- URL: `https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf`
- Página 4 contiene: *"EJECUCIÓN DEL PRESUPUESTO DE GASTOS — Por Niveles del Objeto del Gasto"* con columnas **NIVEL / OBJETO / PRESUPUESTO VIGENTE / OBLIGADO ENE-DIC / % EJEC**.
- Datos verificados en investigación previa (valores en millones de guaraníes):

| Nivel | Objeto | Vigente | Obligado | %Ejec |
|-------|--------|---------|----------|-------|
| 100 | Servicios Personales | 788.089 | 727.234 | 92% |
| 200 | Servicios No Personales | 232.517 | 114.346 | 49% |
| 300 | Bienes de Consumo e Insumos | 205.890 | 79.754 | 39% |
| 500 | Inversión Física | 840.990 | 104.964 | 12% |
| 700 | Servicio de la Deuda Pública | 134.231 | 134.231 | 100% |
| 800 | Transferencias | (dato parcial en PDF) | (65%) | — |
| 900 | Otros Gastos | 24.179 | 5.301 | 22% |
| TOTAL | | 2.360.168 | 1.253.270 | 53% |

(Nota: la fila "Transferencias" mostró datos desalineados en la extracción de texto; el pipeline debe resolverla por coordenadas o marcar incompleta.)

## Modelo de datos (alineado a la fuente)

`data/presupuesto_ejecucion_2024.csv`:

| Columna | Descripción | Disponible |
|---|---|---|
| `ejercicio` | Año fiscal | 2024 |
| `nivel` | Código del objeto del gasto (100,200,...) | ✅ |
| `denominacion` | Nombre del objeto del gasto | ✅ |
| `presupuesto_vigente` | Monto vigente (millones Gs) | ✅ |
| `obligado` | Monto obligado ENE-DIC (millones Gs) | ✅ |
| `porcentaje_ejecucion` | (obligado/vigente)*100 | calculado |
| `fuente` | "Rendición de Cuentas 2024" | ✅ |
| `url` | URL del PDF | ✅ |

**NO disponibles hoy (declarado, no inventado):** `presupuesto_inicial`, `modificacion`, `pagado`, detalle por partida (el inventario FUENTES_2024 los marca como brechas).

## Pipeline

- `scripts/presupuesto_2024.py` (TDD):
  1. Descarga el PDF (o usa copia local en `data/_sin_versionar/`).
  2. Extrae la tabla de la página 4 (por texto/coordenadas según lo exija el layout, con manejo robusto de la fila Transferencias).
  3. Normaliza números (texto → float en millones), incluye % ejecución calculado.
  4. Valida: total vigente = suma de filas; total obligado = suma de filas; % = obligado/vigente.
  5. Escribe `data/presupuesto_ejecucion_2024.csv`.
- Proceso manual primero; automatización tras validar.

## Criterios de éxito

- `scripts/presupuesto_2024.py` pasa sus tests (parsing, validación, totales).
- `data/presupuesto_ejecucion_2024.csv` con las 8 filas (7 niveles + total) y trazabilidad.
- La fila Transferencias queda resuelta o marcada explícitamente como parcial.
- Totales validados (vigente 2.360.168 / obligado 1.253.270 / 53%).
- Sin inventar datos: columnas no disponibles declaradas como brechas.
- Movimiento con la web/lab (sección Gasto) en fase posterior; no se toca aún.

## NO se hace en esta fase

- Hesakã/salarios como dataset (siguiente pipeline).
- DNCP 2024 como dataset (se puede ejecutar el pipeline existente con `anio="2024"`, pero es producto aparte).
- Integración en web/lab.
- Automatización GitHub Actions.