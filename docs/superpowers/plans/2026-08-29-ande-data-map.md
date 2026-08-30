# Data Map ANDE — Inventario de indicadores (Fase 3)

**Fecha:** 2026‑08‑29  
**Estado:** Aprobado (diseño)  
**Fuente primaria:** ANDE (PDF BAGP 2025, Pliego 21, Compilación 2000‑2020)  
**Objetivo:** Catálogo exhaustivo de indicadores eléctricos con metadatos de extracción, formato y prioridad. Sirve de base para el conector, la base de datos y la automatización.

---

## Cuadro de indicadores

| Indicador | Fuente ANDE | Formato | Frecuencia | Histórico | Método de extracción | Prioridad |
|-----------|-------------|---------|------------|-----------|----------------------|-----------|
| Demanda eléctrica | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Demanda máxima (MW) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Factor de carga anual | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Consumo total (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Consumo residencial (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Consumo industrial (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Consumo otros (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Consumo gubernamental (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Baja |
| Consumo diferencial (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Baja |
| Consumo alta tensión (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Consumo muy alta tensión (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Consumo electrointensivas (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Consumo alumbrado público (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Baja |
| Pérdidas totales (GWh) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Pérdidas distribución (%) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Pérdidas transmisión (%) | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Clientes totales | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | **Alta** |
| Evolución de clientes | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Clientes por categoría | BAGP 2025 | PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Tarifas residenciales BT (8 tramos) | Pliego 21 | PDF/HTML | Anual (2025) | 2025 | extracción PDF pdfplumber | **Alta** |
| Generación Itaipú (a PY) (GWh) | BAGP 2025 / itaipu.gov.py | PDF/HTML | Anual (2025) | 2025 | extracción PDF pdfplumber + web | **Alta** |
| Generación Yacyretá (a PY) (GWh) | BAGP 2025 / EBY | PDF/HTML | Anual (2025) | 2025 | extracción PDF pdfplumber + web | **Alta** |
| Generación Yacyretá total (GWh) | BAGP 2025 / EBY | PDF/HTML | Anual (2025) | 2025 | extracción PDF pdfplumber + web | **Alta** |
| Generación Acaray (GWh) | BAGP 2025 | PDF | Período 2000‑2020 | 2000‑2020 | extracción PDF pdfplumber | Baja |
| Factor de carga interanual (%) | Cálculo interno (BAGP + Compilación) | HTML/cálculo | Anual | 2000‑2021 | cálculo interno | Media |
| Series históricas demanda 2000‑2020 | Compilación 2000‑2020 | HTML/PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |
| Series históricas consumo 2000‑2020 | Compilación 2000‑2020 | HTML/PDF | Anual | 2000‑2020 | extracción PDF pdfplumber | Media |

**Notas:**

- **Prioridad Alta** = indicadores críticos para el MVP; se extraerán en la primera fase.
- **Prioridad Media** = indicadores relevantes que se incorporarán en una segunda fase.
- **Prioridad Baja** = indicadores de interés técnico o future‑scope; no bloquean el MVP.
- El **método de extracción** “extracción PDF pdfplumber” cubre la mayoría de los PDFs del BAGP y Pliego 21. Para las series históricas (2000‑2020) se usa el mismo extractor sobre el archivo de compilación.
- La **frecuencia** “anual” cubre la mayoría de los indicadores; el histórico 2000‑2020 abarca la compilación completa.

---

## Propósito del Data Map

1. **Ordena la información** — pasa de “datos sueltos” a un catálogo único.
2. **Define prioridades** — qué indicadores son *Alta* prioridad para el MVP y cuáles pueden esperar.
3. **Guía el extractor** — sin ese mapa, el extractor carece de dirección clara para nuevas actualizaciones.
4. **Facilita la automatización** — el paso 6 (GitHub Actions) necesita saber *qué* extraer, *con qué frecuencia* y con *método* definido.

**Próximo paso:** una vez fijado el Data Map, se procederá a la generación del archivo MVP (`www/datos/ande-indicadores-mvp.json`) y a la configuración del workflow de GitHub Actions para la actualización automática.

---
*Este documento forma parte del plan de migración `2026-08-29-muchotexto-data-migracion.md` y forma parte del repositorio `Datos Públicos` (no versionado en el sentido principal, pero rastreado para control interno).*