import os
import unittest
from .. import extractor

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "nota_2025.html")


class TestExtractNota2025(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE, encoding="utf-8") as f:
            self.html = f.read()

    def test_extract_consumo(self):
        recs = extractor.extract(self.html)
        consumo = next(r for r in recs if r["indicador"] == "consumo_total")
        self.assertEqual(consumo["valor_raw"], "29.419")
        self.assertEqual(consumo["unidad"], "GWh")

    def test_extract_demanda(self):
        recs = extractor.extract(self.html)
        demanda = next(r for r in recs if r["indicador"] == "demanda_maxima")
        self.assertEqual(demanda["valor_raw"], "5.280")
        self.assertEqual(demanda["unidad"], "MW")

    def test_extract_generacion(self):
        recs = extractor.extract(self.html)
        gen = {r["indicador"]: r["valor_raw"] for r in recs
               if r["indicador"].startswith("generacion_")}
        self.assertEqual(gen["generacion_itaipu"], "25.768")
        self.assertEqual(gen["generacion_yacyreta"], "3.081")
        self.assertEqual(gen["generacion_acaray"], "570")


if __name__ == "__main__":
    unittest.main()
