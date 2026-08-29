import os
import unittest
from unittest import mock
from .. import connector, extractor

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")
URL = "https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf"


def _load(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


class TestRunPdf(unittest.TestCase):
    def test_run_pdf_uses_parsers(self):
        texto = "\n".join([
            _load("pdf_consumo_categoria.txt"),
            _load("pdf_tarifas.txt"),
            _load("pdf_perdidas.txt"),
            _load("pdf_clientes.txt"),
        ])
        with mock.patch.object(extractor, "pdf_text", return_value=texto):
            recs = connector.run_pdf("falso.pdf", url=URL)
        indicadores = {r["indicador"]: r for r in recs}
        # consumo por categoría normalizado a GWh
        self.assertEqual(indicadores["consumo_categoria_residencial"]["valor"], 9500.0)
        self.assertEqual(indicadores["consumo_categoria_residencial"]["unidad"], "GWh")
        # pérdidas como porcentaje
        self.assertEqual(indicadores["perdidas_totales"]["valor"], 24.4)
        self.assertEqual(indicadores["perdidas_totales"]["unidad"], "%")
        # clientes
        self.assertEqual(indicadores["clientes_total"]["valor"], 3200000.0)
        self.assertEqual(indicadores["clientes_nuevos"]["valor"], 28000.0)


if __name__ == "__main__":
    unittest.main()
