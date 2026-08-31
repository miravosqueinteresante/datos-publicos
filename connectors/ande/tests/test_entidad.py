import unittest
from .. import entidad


class TestEntidad(unittest.TestCase):
    def test_get_por_id(self):
        e = entidad.get("ande")
        self.assertEqual(e["nombre"], "Administración Nacional de Electricidad")
        self.assertEqual(e["tipo"], "estatal")

    def test_get_por_id_itaipu(self):
        e = entidad.get("itaipu")
        self.assertEqual(e["sigla"], "ITAIPU")

    def test_get_inexistente(self):
        e = entidad.get("noexiste")
        self.assertIsNone(e)

    def test_listar_ids(self):
        ids = entidad.listar_ids()
        self.assertIn("ande", ids)
        self.assertIn("itaipu", ids)
        self.assertIn("yacyreta", ids)

    def test_nombre_a_id(self):
        eid = entidad.nombre_a_id("ANDE")
        self.assertEqual(eid, "ande")

    def test_nombre_a_id_case_insensitive(self):
        eid = entidad.nombre_a_id("itaipú")
        self.assertEqual(eid, "itaipu")

    def test_nombre_a_id_desconocido(self):
        eid = entidad.nombre_a_id("Entidad Desconocida")
        self.assertIsNone(eid)


if __name__ == "__main__":
    unittest.main()
