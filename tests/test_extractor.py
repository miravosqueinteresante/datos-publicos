import os, unittest
from connectors.yacyreta import extractor
FIX = os.path.join(os.path.dirname(__file__), "..", "connectors", "yacyreta", "fixtures", "yacyreta_anual2020.html")
class TestExtractorAnnual(unittest.TestCase):
    def test_extract_annual(self):
        with open(FIX, encoding="utf-8") as f:
            h = f.read()
        r = extractor.extract_annual(h)
        self.assertIsNotNone(r)
        self.assertAlmostEqual(r["total_mwh"], 14857292, places=0)
        self.assertAlmostEqual(r["sinp_mwh"], 1664316.8, places=1)
        self.assertAlmostEqual(r["sadi_mwh"], 13192975.2, places=1)
if __name__ == "__main__":
    unittest.main()
