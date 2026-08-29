import os
import tempfile
import unittest
from .. import connector

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "nota_2025.html")
URL = "https://www.ande.gov.py/interna.php?id=14877"


class TestPipeline(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE, encoding="utf-8") as f:
            self.html = f.read()

    def test_run_produces_records(self):
        recs = connector.run(self.html, url=URL)
        self.assertEqual(len(recs), 5)

    def test_consumo_normalized_to_gwh(self):
        recs = connector.run(self.html, url=URL)
        consumo = next(r for r in recs if r["indicador"] == "consumo_total")
        self.assertEqual(consumo["valor"], 29419.0)
        self.assertEqual(consumo["unidad"], "GWh")

    def test_demanda_kept_as_mw(self):
        recs = connector.run(self.html, url=URL)
        demanda = next(r for r in recs if r["indicador"] == "demanda_maxima")
        self.assertEqual(demanda["valor"], 5280.0)
        self.assertEqual(demanda["unidad"], "MW")

    def test_schema_fields_present(self):
        recs = connector.run(self.html, url=URL)
        rec = recs[0]
        for field in ("id", "entidad", "indicador", "valor", "unidad",
                      "fecha_inicio", "fecha_fin", "fuente", "url",
                      "fecha_extraccion", "metodo_extraccion", "estado_verificacion"):
            self.assertIn(field, rec)

    def test_store_writes_json(self):
        recs = connector.run(self.html, url=URL)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.json")
            connector.store(recs, path)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
