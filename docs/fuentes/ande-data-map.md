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
| Generación / abastecimiento (Itaipú, Yacyretá, Acaray) | Compilación Estadística 2000–2020 (cuadro "Origen de la Energía"); `generacion.php`; Memoria Anual | PDF + HTML | Anual (serie 2000–2020) | Sí | Tablas PDF (serie validada, combinada) | Alta |
| Pérdidas (total / distribución / transmisión) | BAGP 2025; Plan Maestro Pérdidas; nota `interna.php?id=15116` | PDF + HTML | Mensual + año móvil | Sí | PDF + notas mensuales | Alta |
| Tarifas (categoría, tensión, precio, resolución) | `tarifas_vigentes.php`; Pliego Nº 21 + resoluciones | HTML + PDF | Por resolución (sin calendario) | Sí (histórico de resoluciones) | HTML tabla + PDF pliego | Alta |
| Consumidores intensivos especiales (GCIE) | RP 47191/2022, RP 49238/2024; Pliego Nº 21 (cat. 911–920) | PDF | Por resolución | Sí | Resoluciones PDF | Alta |
| Clientes (total / evolución / categoría) | BAGP 2025 (cuadro Consumo por categoría, col. Cantidad de Usuarios); Memoria Anual; MEF Balance | PDF | Anual | Parcial | Tabla PDF (total validado; por categoría pendiente) | Media |
| Factor de carga anual (SIN) | BAGP 2025 (cuadro Consumo/Demanda/Factor de Carga del SIN) | PDF | Anual | Sí | Tabla PDF | Media |

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
- **Nota oficial `interna.php?id=14877` es renderizada por JS**: su HTML no contiene las cifras en texto
  plano, por lo que el conector HTML no las recupera. Las cifras de consumo/demanda/factor se validaron
  contra el **BAGP 2025 (cuadro del SIN)**, fuente primaria y oficial.
- **Generación — RESUELTA (combinada, serie 2000–2020)**: la Compilación Estadística 2000–2020 trae el
  cuadro "Origen de la Energía" con dos series validadas: `generacion_binacional_itaipu_yacyreta`
  ("Energía Comprada (Itaipú y Yacyretá)") y `generacion_nacional_acaray_termicas` ("Generación Bruta
  (Acaray y Térmicas)"), en MWh→GWh. `generacion.php` es JS-renderizado sin datos; se descartó.
- **Generación por central individual (2025) — RESUELTA parcialmente (curada)**: Itaipú y Yacyretá
  publican sus cifras 2025 en fuentes primarias. `generacion_itaipu_paraguay` = 25.768 GWh (energía
  suministrada a Paraguay, itaipu.gov.py 09/01/2026) y `generacion_yacyreta_paraguay` = 3.081 GWh
  (energía retirada por ANDE, EBY vía prensa), más `generacion_yacyreta_total` = 16.103 GWh. Se integran
  como registros **curados/verificados** (`extraccion_manual`) con su URL de procedencia, no por scraper.
- **Acaray 2025 (por central) — BRECHA FINA**: la Compilación trae "Acaray + Térmicas" combinado (serie
  2000–2020), pero no el valor 2025 de Acaray aislado. Requiere Memoria Anual 2025 de ANDE. Mientras tanto
  queda fuera del dataset publicado.
- **Generación año 2025 combinada vs serie histórica**: la serie 2000–2020 (Compilación) y los valores
  curados 2025 (binacionales) son métricas distintas y años distintos; conviven etiquetadas en el dataset.
- **Frecuencia mensual no estructurada**: consumo y demanda mensuales solo circulan como cifras sueltas
  en notas de prensa (ej. enero–mayo 2026 = 14.587,1 GWh, +19,4%). No hay serie mensual descargable →
  brecha de trazabilidad para granularidad mensual.
- **Clientes por categoría**: el BAGP 2025 trae la columna "Cantidad de Usuarios" por grupo, pero el
  conector solo publica el total (1.680.946). La desagregación por categoría queda para una 2ª pasada.
- **Fuente complementaria (no ANDE)**: el Viceministerio de Minas y Energía publica el Balance
  Energético Nacional (VMME-MOPC, PDF anual). Es candidato a un conector futuro, no fuente primaria de ANDE.

---

## Valores validados 2025 (extraídos y contrastados con BAGP 2025 / Pliego 21)
- Consumo total (SIN): **29.419 GWh** (29.418.538 MWh) — BAGP 2025, cuadro SIN
- Demanda máxima (SIN): **5.280 MW** (15 dic 2025) — BAGP 2025, cuadro SIN
- Factor de carga anual: **63,60%** — BAGP 2025, cuadro SIN
- Pérdidas totales (año móvil, dic-2025): **24,40%** (distribución **21,89%**, transmisión 4,37%) — BAGP 2025
- Clientes totales: **1.680.946** — BAGP 2025, cuadro Consumo por categoría
- Consumo por categoría (GWh): Residencial 7.426 · Electrointensivas 5.465 · Otros 6.842 · Industrial 267 ·
  Gubernamental 443 · Muy alta tensión 253 · Alta tensión 886 · Diferencial 101 · Alumbrado público 236
- Tarifa residencial BT (Pliego 21, G/kWh): 0–50=311,55 · 51–150=349,89 · 151–300=365,45 ·
  301–500=403,82 · 501–1000=420,27 · >1000=435,51

Estos valores se usan como assert de validación: si el extractor difiere del orden de magnitud, marca
"cambio anormal" (§12 del maestro) en lugar de corregir silenciosamente.
