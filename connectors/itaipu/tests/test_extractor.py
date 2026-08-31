import os
import unittest
from .. import extractor

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "itaipu_sample.csv")


class TestExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIXTURE, encoding="utf-8") as f:
            cls.rows = extractor.parse_csv(f.read())

    def test_parse_returns_list(self):
        self.assertIsInstance(self.rows, list)

    def test_parse_extracts_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_row_has_required_fields(self):
        row = self.rows[0]
        for field in ("din_instante", "val_itaipu_total", "val_itaipu_50hz"):
            self.assertIn(field, row)

    def test_values_are_floats(self):
        row = self.rows[0]
        self.assertIsInstance(row["val_itaipu_total"], float)

    def test_date_parsed(self):
        row = self.rows[0]
        self.assertEqual(row["din_instante"].year, 2024)


if __name__ == "__main__":
    unittest.main()
