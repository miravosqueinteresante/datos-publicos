# ANDE Data Map — MuchoTexto Data

> Primer documento técnico del conector ANDE. Inventario indicador por indicador según el
> esquema del Documento Maestro (§35). Es la especificación del conector: de aquí salen el
> extractor, el esquema de la base y la automatización.

**Investigación:** 2026-08-29 (ver `research_ande/findings_*.md` para fuentes y citas).
**Hallazgo estructural clave:** ANDE **no expone API ni CSV** en ningún canal revisado. Todos los
datos están en **PDF** (Memoria Anual, Resumen Estadístico, Compilación Estadística, BAGP, Plan
Maestro) o **HTML** (notas de prensa, `generacion.php`, `tarifas_vigentes.php`). El conector debe
extraer de PDF/HTML conservando URL + fecha de obtención (principio de trazabilidad del proyecto).

---

## Mapa de indicadores

| Indicador | Fuente ANDE | Formato | Frecuencia | Histórico | Método de extracción | Prioridad |
|---|---|---|---|---|---|---|
| Demanda máxima (SIN, MW) | Memoria Anual; nota `interna.php?id=14877` | PDF + HTML | Anual (récords por prensa) | Sí | Tabla PDF + captura de notas de récord | Alta |
| Consumo total / energía demandada (GWh) | Memoria Anual; Resumen Estadístico; nota `interna.php?id=14877` | PDF + HTML | Anual | Sí | Tabla PDF | Alta |
| Consumo por categoría (grupo de consumo) | Memoria Anual (Energía Facturada por Grupo de Consumo) | PDF | Anual | Sí | Tablas PDF por grupo | Alta |
| Generación / abastecimiento (Itaipú, Yacyretá, Acaray) | `generacion.php`; Memoria Anual | HTML + PDF | Anual | Sí | Fichas HTML + tablas PDF | Alta |
| Pérdidas (total / distribución / transmisión) | BAGP 2025; Plan Maestro Pérdidas; nota `interna.php?id=15116` | PDF + HTML | Mensual + año móvil | Sí | PDF + notas mensuales | Alta |
| Tarifas (categoría, tensión, precio, resolución) | `tarifas_vigentes.php`; Pliego Nº 21 + resoluciones | HTML + PDF | Por resolución (sin calendario) | Sí (histórico de resoluciones) | HTML tabla + PDF pliego | Alta |
| Consumidores intensivos especiales (GCIE) | RP 47191/2022, RP 49238/2024; Pliego Nº 21 (cat. 911–920) | PDF | Por resolución | Sí | Resoluciones PDF | Alta |
| Clientes (total / evolución / categoría) | BAGP 2025; Memoria Anual; MEF Balance | PDF | Anual | Parcial | PDF (pendiente 2ª pasada) | Media |

### Fuentes primarias (URLs)
- Memoria Anual / estados contables: `https://www.ande.gov.py/contables.php?cat=5`
- Resumen Estadístico 2020–2024: `https://www.ande.gov.py/finanzas/ANDE%20-%20Resumen%20Estad%C3%ADstico%202020%20-%202024.pdf`
- Compilación Estadística 2000–2020 (serie larga): `https://www.ande.gov.py/documentos_contables/747/ande_-_compilacion_estadistica_2000-2020.pdf`
- Generación / oferta-demanda: `https://www.ande.gov.py/generacion.php`
- Tarifas vigentes: `https://www.ande.gov.py/tarifas_vigentes.php` · Pliego: `https://www.ande.gov.py/docs/tarifas/`
- BAGP 2025: `https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf`
- Plan Maestro Pérdidas 2025: `https://www.ande.gov.py/documentos/plan_maestro/Plan%20de%20Reduccion%20de%20Perdidas%202025.pdf`
- Nota oficial pérdidas/clientes: `https://www.ande.gov.py/interna.php?id=15116`
- Nota oficial consumo/demanda 2025: `https://www.ande.gov.py/interna.php?id=14877`

---

## Brechas / limitaciones (transparencia, §31 del maestro)
- **Sin API ni CSV**: todo por extracción de PDF/HTML. La extracción debe conservar la referencia exacta.
- **Frecuencia mensual no estructurada**: consumo y demanda mensuales solo circulan como cifras sueltas
  en notas de prensa (ej. enero–mayo 2026 = 14.587,1 GWh, +19,4%). No hay serie mensual descargable →
  brecha de trazabilidad para granularidad mensual.
- **Clientes**: la serie numérica (total y por categoría) no fue extraída aún (límite de la búsqueda);
  las fuentes oficiales donde debe estar (BAGP 2025, Memoria Anual, MEF) están identificadas para una
  segunda pasada.
- **Fuente complementaria (no ANDE)**: el Viceministerio de Minas y Energía publica el Balance
  Energético Nacional (VMME-MOPC, PDF anual). Es candidato a un conector futuro, no fuente primaria de ANDE.

---

## Valores de referencia 2025 (para validar el extractor en Fase 4)
- Consumo total: **29.419 GWh** (+12,5% interanual) — `interna.php?id=14877`
- Demanda máxima: **5.280 MW** (15 dic 2025) — `interna.php?id=14877`
- Abastecimiento: Itaipú 25.768 GWh (87,6%), Yacyretá 3.081 GWh (10,5%), Acaray 570 GWh (1,9%)
- Pérdidas totales (año móvil, dic-2025): **24,40%** (distribución 20,03%, transmisión 4,37%) — BAGP 2025
- Nuevos clientes 2025: ~28.000 familias — `interna.php?id=15116`

Estos valores se usan como assert de validación: si el extractor difiere del orden de magnitud, marca
"cambio anormal" (§12 del maestro) en lugar de corregir silenciosamente.
