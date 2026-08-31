import unittest
from .. import curados


class TestCurados(unittest.TestCase):
    def test_tres_registros(self):
        self.assertEqual(len(curados.CURADOS), 3)

    def test_valores_y_estado(self):
        d = {r["indicador"]: r for r in curados.CURADOS}
        self.assertEqual(d["generacion_itaipu_paraguay"]["valor"], 25768.0)
        self.assertEqual(d["generacion_itaipu_paraguay"]["unidad"], "GWh")
        self.assertEqual(d["generacion_itaipu_paraguay"]["estado_verificacion"], "verificado")
        self.assertEqual(d["generacion_yacyreta_paraguay"]["valor"], 3081.0)
        self.assertEqual(d["generacion_yacyreta_total"]["valor"], 16103.0)
        for r in curados.CURADOS:
            self.assertTrue(r["url"].startswith("http"))

    def test_entidad_ids_correctos(self):
        d = {r["indicador"]: r for r in curados.CURADOS}
        self.assertEqual(d["generacion_itaipu_paraguay"]["entidad_id"], "itaipu")
        self.assertEqual(d["generacion_yacyreta_paraguay"]["entidad_id"], "yacyreta")
        self.assertEqual(d["generacion_yacyreta_total"]["entidad_id"], "yacyreta")

    def test_entidad_names_correctos(self):
        d = {r["indicador"]: r for r in curados.CURADOS}
        self.assertEqual(d["generacion_itaipu_paraguay"]["entidad"], "Itaipú Binacional")
        self.assertEqual(d["generacion_yacyreta_paraguay"]["entidad"], "Entidad Binacional Yacyretá")


if __name__ == "__main__":
    unittest.main()
