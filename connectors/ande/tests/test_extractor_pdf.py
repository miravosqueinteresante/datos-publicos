import os
import unittest
from .. import extractor

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _load(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


class TestExtractConsumoCategoria(unittest.TestCase):
    def test_extrae_todos_los_grupos(self):
        recs = extractor.extract_consumo_categoria(_load("pdf_consumo_categoria.txt"))
        self.assertEqual(len(recs), 9)

    def test_residencial(self):
        recs = extractor.extract_consumo_categoria(_load("pdf_consumo_categoria.txt"))
        r = next(x for x in recs if x["indicador"] == "consumo_categoria_residencial")
        self.assertEqual(r["valor_raw"], "9.500.000")
        self.assertEqual(r["unidad"], "MWh")


class TestExtractTarifas(unittest.TestCase):
    def test_residencial_bt_0_50(self):
        recs = extractor.extract_tarifas(_load("pdf_tarifas.txt"))
        r = next(x for x in recs if x["indicador"] == "tarifa_residencial_bt_0_50")
        self.assertEqual(r["valor_raw"], "311,55")
        self.assertEqual(r["unidad"], "G/kWh")

    def test_cuenta_seis_tramos(self):
        recs = extractor.extract_tarifas(_load("pdf_tarifas.txt"))
        self.assertEqual(len(recs), 6)


class TestExtractPerdidas(unittest.TestCase):
    def test_totales(self):
        recs = extractor.extract_perdidas(_load("pdf_perdidas.txt"))
        r = next(x for x in recs if x["indicador"] == "perdidas_totales")
        self.assertEqual(r["valor_raw"], "24,40")
        self.assertEqual(r["unidad"], "%")

    def test_distribucion_y_transmision(self):
        recs = extractor.extract_perdidas(_load("pdf_perdidas.txt"))
        d = next(x for x in recs if x["indicador"] == "perdidas_distribucion")
        t = next(x for x in recs if x["indicador"] == "perdidas_transmision")
        self.assertEqual(d["valor_raw"], "20,03")
        self.assertEqual(t["valor_raw"], "4,37")


class TestExtractClientes(unittest.TestCase):
    def test_total(self):
        recs = extractor.extract_clientes(_load("pdf_clientes.txt"))
        r = next(x for x in recs if x["indicador"] == "clientes_total")
        self.assertEqual(r["valor_raw"], "3.200.000")

    def test_nuevos(self):
        recs = extractor.extract_clientes(_load("pdf_clientes.txt"))
        r = next(x for x in recs if x["indicador"] == "clientes_nuevos")
        self.assertEqual(r["valor_raw"], "28.000")


if __name__ == "__main__":
    unittest.main()
