# Datos Públicos — Inventario documental del ciclo presupuestario 2024 (FUENTES_2024.md)

Fecha: 2026-08-26

## Propósito

Crear el primer entregable del módulo presupuestario: **`docs/presupuesto/FUENTES_2024.md`**, un inventario de fuentes para reconstruir el ciclo presupuestario de la **Municipalidad de Asunción del ejercicio 2024**, siguiendo el documento de contexto "Reconstrucción y análisis del ciclo presupuestario de la Municipalidad de Asunción".

**Regla del documento (sección 29):** no programar aún, no diseñar gráficos; primero responder, documento por documento, qué existe, en qué formato y qué cubre.

## Alcance

**Incluye (solo ciclo presupuestario 2024 Muni):**
- Ordenanza de presupuesto 2024.
- Presupuesto aprobado (por programa, dependencia, objeto del gasto, ingresos).
- Modificaciones presupuestarias 2024.
- Ejecución presupuestaria 2024 (obligado/pagado).
- Rendición de cuentas 2024.
- Remuneraciones/salarios (Hesakã / nómina).
- Transferencias del Estado a la Muni (MEF).
- Contrataciones DNCP 2024 (ya pipelinezables).

**Excluye (no en esta fase):**
- Fuentes complementarias de cruce (CGR, SFP, otros) — se documentan solo si aportan al ciclo.
- Construcción del pipeline/modelo de datos (post-inventario).
- Cualquier dato no relacionado con la Muni o con 2024.

## Estructura del entregable

El documento de ideas propone por fuente: **ID · Documento · Fuente · Período · Formato · Contenido · Estado**. Se adopta esa tabla, ampliada con trazabilidad (URL, fecha de verificación, método) según las convenciones del proyecto.

`docs/presupuesto/FUENTES_2024.md` con:
1. Resumen ejecutivo (qué se encontró y qué no).
2. Tabla de fuentes del ciclo (ID P01..Pn).
3. Ficha de evidencia por fuente (URL, formato, cobertura, accesibilidad, automatización posible, limitaciones).
4. Map de fuentes al ciclo: Aprobado → Modificaciones → Vigente → Ejecución → Pagos.
5. Brechas y próximos pasos (modelo de datos propuesto en el documento).

## Criterios de éxito

- `docs/presupuesto/FUENTES_2024.md` existe, en español, con trazabilidad (URL + fecha de verificación).
- Cubre las fuentes del alcance con estado verificado/investigado.
- Distingue explícitamente lo **disponible** de lo **no verificado/bloqueado** (no inventar).
- No se programó nada (solo documentación).
- Todo versionado y pusheado.