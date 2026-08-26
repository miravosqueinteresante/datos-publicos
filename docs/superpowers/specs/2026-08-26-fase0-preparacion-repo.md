# Datos Públicos — FASE 0: Preparación del repositorio

Fecha: 2026-08-26

## Propósito

Crear la infraestructura inicial del proyecto Datos Públicos: un repositorio Git único en GitHub, con estructura de carpetas, convenciones y documentación base. Sin construir webs ni pipelines todavía — eso viene después, según el plan maestro.

## Contexto

- **Nombre:** Datos Públicos
- **Laboratorio:** lab.muchotexto.net
- **Plataforma pública:** datospublicos.muchotexto.net
- **Primer caso de uso:** Municipalidad de Asunción
- **Cuenta GitHub:** miravosqueinteresante
- **Carpeta local:** `C:\Users\pc\Desktop\Proyectos\Datos Publicos` (nombre con espacio)
- **Asistente de desarrollo:** OpenCode

## Decisiones cerradas

1. **Un solo repositorio** llamado `datos-publicos`. El plan maestro (sección 7) define que lab y plataforma son dos interfaces de un mismo sistema, no dos proyectos.
2. **Carpeta local actual** (`Datos Publicos`) como raíz de trabajo. El nombre local difiere del nombre del repo remoto, lo cual es normal en Git.
3. **El plan maestro es SOLO LOCAL.** No se versiona, no se sube a GitHub, no se transcribe a `docs/`. El PDF vive fuera del área de trabajo del repo.
4. **Estructura de GitHub Pages:** las webs `lab/` y `www/` se sirven desde subcarpetas del repo único. No se configuran todavía (según el plan, primero el pipeline real).

## Estructura de carpetas

```
datos-publicos/
├── README.md              # Qué es, estado, cómo empezar
├── AGENTS.md              # Convenciones + regla del plan local
├── .gitignore             # Ignora el plan maestro si estuviera dentro
├── docs/                  # Documentación del proyecto
│   └── superpowers/       # specs + plans
├── data/                  # Datasets procesados (versionados)
├── scripts/               # Pipelines y herramientas (Python)
├── lab/                   # web del laboratorio (GitHub Pages)
├── www/                   # web de la plataforma pública (GitHub Pages)
└── .github/workflows/     # GitHub Actions (automatización)
```

## Alcance del primer hito

1. Crear el repositorio en GitHub (`gh repo create datos-publicos`).
2. `git init` en la carpeta local.
3. Crear `README.md`, `AGENTS.md`, `.gitignore`.
4. Estructura base de carpetas.
5. Primer commit + push a `main`.

**NO se hace en esta fase:**
- Configurar GitHub Pages / CNAME de los dominios.
- Construir las webs.
- Escribir pipelines.
- Inventario de datos (FASE 1).

## Regla sobre el Plan Maestro (obligatoria)

El documento `DATOS PÚBLICOS — DOCUMENTO MAESTRO DEL PROYECTO.pdf` es interno y solo local.

- No debe añadirse al repositorio bajo ninguna circunstancia.
- No debe transcribirse a `docs/` ni a ningún archivo versionado.
- Debe documentarse en `AGENTS.md` para que ningún agente o editor lo suba.
- El `.gitignore` incluirá una entrada para ignorarlo si alguna vez estuviera dentro del repo (defensa en profundidad).

## Criterios de éxito

- El repositorio `datos-publicos` existe en GitHub con el primer commit en `main`.
- La estructura base está creada y limpia.
- `AGENTS.md` documenta la regla del plan maestro.
- `README.md` describe el proyecto y su estado.
- Nada del plan maestro está en el repo remoto.
