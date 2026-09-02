import json
import os
import unittest
from .. import extractor

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _tables(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return json.load(f)


def _text(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


BAGP_TABLES = _tables("bagp2025_tables.json")
BAGP_TEXT = _text("bagp2025_text.txt")
PLIEGO_TABLES = _tables("pliego21_tables.json")


class TestExtractConsumoCategoria(unittest.TestCase):
    def test_nueve_grupos(self):
        recs = extractor.extract_consumo_categoria(BAGP_TABLES)
        self.assertEqual(len(recs), 9)

    def test_residencial(self):
        recs = extractor.extract_consumo_categoria(BAGP_TABLES)
        r = next(x for x in recs if x["indicador"] == "consumo_categoria_residencial")
        self.assertEqual(r["valor_raw"], "7.425.632.545")
        self.assertEqual(r["unidad"], "kWh")


class TestExtractClientes(unittest.TestCase):
    def test_total_real(self):
        recs = extractor.extract_clientes(BAGP_TABLES)
        r = next(x for x in recs if x["indicador"] == "clientes_total")
        self.assertEqual(r["valor_raw"], "1.680.946")

    def test_categoria_residencial(self):
        recs = extractor.extract_clientes_categoria(BAGP_TABLES)
        r = next(x for x in recs if x["indicador"] == "clientes_categoria_residencial")
        self.assertEqual(r["valor_raw"], "1.482.966")
        self.assertEqual(r["unidad"], "clientes")

    def test_ocho_categorias(self):
        recs = extractor.extract_clientes_categoria(BAGP_TABLES)
        self.assertEqual(len(recs), 8)


class TestExtractPerdidas(unittest.TestCase):
    def test_totales(self):
        recs = extractor.extract_perdidas(BAGP_TEXT)
        r = next(x for x in recs if x["indicador"] == "perdidas_totales")
        self.assertEqual(r["valor_raw"], "24,40")

    def test_distribucion_y_transmision(self):
        recs = extractor.extract_perdidas(BAGP_TEXT)
        d = next(x for x in recs if x["indicador"] == "perdidas_distribucion")
        t = next(x for x in recs if x["indicador"] == "perdidas_transmision")
        self.assertEqual(d["valor_raw"], "20,03")
        self.assertEqual(t["valor_raw"], "4,37")


class TestExtractSinIndicators(unittest.TestCase):
    def test_consumo_y_demanda(self):
        recs = {r["indicador"]: r for r in extractor.extract_sin_indicators(BAGP_TABLES)}
        self.assertEqual(recs["consumo_total"]["valor_raw"], "29.418.538")
        self.assertEqual(recs["consumo_total"]["unidad"], "MWh")
        self.assertEqual(recs["demanda_maxima"]["valor_raw"], "5.280")
        self.assertEqual(recs["factor_carga"]["valor_raw"], "63,60")


class TestExtractTarifas(unittest.TestCase):
    def test_residencial_bt_0_50(self):
        recs = extractor.extract_tarifas(PLIEGO_TABLES)
        r = next(x for x in recs if x["indicador"] == "tarifa_residencial_bt_0_50")
        self.assertEqual(r["valor_raw"], "311,55")
        self.assertEqual(r["unidad"], "G/kWh")

    def test_seis_tramos(self):
        recs = extractor.extract_tarifas(PLIEGO_TABLES)
        self.assertEqual(len(recs), 6)


class TestExtractGeneracionSerie(unittest.TestCase):
    def test_serie_2000_2020(self):
        tabla = _tables("compilacion_generacion_table.json")
        recs = extractor.extract_generacion_serie([tabla])
        self.assertEqual(len(recs), 42)

    def test_ultimo_ano_binacional(self):
        tabla = _tables("compilacion_generacion_table.json")
        recs = {(r["periodo_text"], r["indicador"]): r
                for r in extractor.extract_generacion_serie([tabla])}
        r = recs[("2020", "generacion_binacional_itaipu_yacyreta")]
        self.assertEqual(r["valor_raw"], "17.525.615")
        self.assertEqual(r["unidad"], "MWh")


if __name__ == "__main__":
    unittest.main()
