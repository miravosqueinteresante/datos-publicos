import unittest
from .. import metadata


class TestEntidadSchema(unittest.TestCase):
    def test_build_record_incluye_entidad_id(self):
        rec = metadata.build_record(
            "test_ind", 100, "GWh", "2025",
            fuente="Test", url="http://test.com", entidad="ANDE")
        self.assertIn("entidad_id", rec)
        self.assertEqual(rec["entidad_id"], "ande")

    def test_build_record_id_incluye_entidad_id(self):
        rec = metadata.build_record(
            "test_ind", 100, "GWh", "2025",
            fuente="Test", url="http://test.com", entidad="ANDE")
        self.assertTrue(rec["id"].startswith("ande-"))

    def test_entidad_no_encontrada_fallback_ande(self):
        rec = metadata.build_record(
            "test_ind", 100, "GWh", "2025",
            fuente="Test", url="http://test.com", entidad="INVENTADA")
        self.assertEqual(rec["entidad_id"], "ande")

    def test_entidad_numerica_se_usa_directamente(self):
        rec = metadata.build_record(
            "test_ind", 100, "GWh", "2025",
            fuente="Test", url="http://test.com", entidad=42)
        self.assertEqual(rec["entidad_id"], 42)
        self.assertTrue(rec["id"].startswith("42-test_ind-"))


if __name__ == "__main__":
    unittest.main()
