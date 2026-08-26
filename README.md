# Datos Públicos

Infraestructura cívica de datos abiertos. Toma información pública dispersa y la transforma
en datos estructurados, indicadores, visualizaciones y herramientas útiles.

## Sitios

- **Laboratorio:** lab.muchotexto.net (cómo funciona el sistema)
- **Plataforma pública:** datospublicos.muchotexto.net (qué puede hacer la gente con la información)

## Primer caso de uso

Municipalidad de Asunción. La arquitectura está pensada para extenderse a otros municipios.

## Estado

**FASE 0 — Preparación (en curso):** repositorio, estructura y convenciones.

Próximas fases:
1. Inventario de datos municipales
2. Evaluación de fuentes
3. Primera fuente y primer pipeline
4. Primer producto útil

## Estructura

- `docs/` — documentación del proyecto (specs y planes en `docs/superpowers/`)
- `data/` — datasets procesados
- `scripts/` — pipelines y herramientas
- `lab/` — web del laboratorio
- `www/` — web de la plataforma pública
- `.github/workflows/` — automatización (GitHub Actions)

## Regla importante

El **documento maestro** del proyecto es interno y de distribución limitada: vive solo en local
y NO se versiona ni se publica en este repositorio.
