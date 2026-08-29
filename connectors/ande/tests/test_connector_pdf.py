import json
import os
import unittest
from .. import connector

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")
URL_BAGP = "https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf"
URL_PLIEGO = "https://www.ande.gov.py/docs/tarifas/PLIEGO21.pdf"


def _tables(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return json.load(f)


def _text(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


class TestRunPdf(unittest.TestCase):
    def test_bagp_y_pliego(self):
        recs = connector._run_pdf_parts(
            _text("bagp2025_text.txt"), _tables("bagp2025_tables.json"), URL_BAGP)
        recs += connector._run_pdf_parts(
            "", _tables("pliego21_tables.json"), URL_PLIEGO)
        ind = {r["indicador"]: r for r in recs}

        self.assertEqual(ind["consumo_categoria_residencial"]["valor"], 7425.632545)
        self.assertEqual(ind["consumo_categoria_residencial"]["unidad"], "GWh")
        self.assertEqual(ind["perdidas_totales"]["valor"], 24.4)
        self.assertEqual(ind["perdidas_totales"]["unidad"], "%")
        self.assertEqual(ind["clientes_total"]["valor"], 1680946.0)
        self.assertEqual(ind["consumo_total"]["valor"], 29418.538)
        self.assertEqual(ind["consumo_total"]["unidad"], "GWh")
        self.assertEqual(ind["demanda_maxima"]["valor"], 5280.0)
        self.assertEqual(ind["factor_carga"]["valor"], 63.6)
        self.assertEqual(ind["tarifa_residencial_bt_0_50"]["valor"], 311.55)
        self.assertEqual(ind["tarifa_residencial_bt_0_50"]["unidad"], "G/kWh")

    def test_sin_duplicados(self):
        recs = connector._run_pdf_parts(
            _text("bagp2025_text.txt"), _tables("bagp2025_tables.json"), URL_BAGP)
        self.assertEqual(len(recs), len({(r["indicador"], r["fecha_inicio"]) for r in recs}))


if __name__ == "__main__":
    unittest.main()
