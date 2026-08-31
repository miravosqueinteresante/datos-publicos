import os
import tempfile
import unittest
from .. import connector

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "itaipu_sample.csv")


class TestConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIXTURE, encoding="utf-8") as f:
            text = f.read()
        cls.rows = connector.extract(text)
        cls.normalized = connector.normalize(cls.rows)
        cls.records = connector.build(cls.normalized)

    def test_extract_returns_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_normalize_returns_yearly(self):
        self.assertGreater(len(self.normalized), 0)

    def test_build_returns_records(self):
        self.assertGreater(len(self.records), 0)

    def test_record_has_required_fields(self):
        rec = self.records[0]
        for field in ("id", "entidad", "entidad_id", "indicador", "valor", "unidad",
                      "fecha_inicio", "fecha_fin", "fuente", "url",
                      "fecha_extraccion", "metodo_extraccion", "estado_verificacion"):
            self.assertIn(field, rec)

    def test_record_entidad_is_itaipu(self):
        rec = self.records[0]
        self.assertEqual(rec["entidad"], "Itaipú Binacional")
        self.assertEqual(rec["entidad_id"], "itaipu")

    def test_store_writes_json(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.json")
            connector.store(self.records, path)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
