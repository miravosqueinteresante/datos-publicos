import os, unittest
from .. import extractor
FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures", "yacyreta_nov2023.html")
class TestExtractor(unittest.TestCase):
    def test_extract_month(self):
        with open(FIX, encoding="utf-8") as f:
            h = f.read()
        r = extractor.extract_month(h)
        self.assertAlmostEqual(r["total_mwh"], 1783337.7, places=1)
        self.assertAlmostEqual(r["sadi_mwh"], 1549645.8, places=1)
        self.assertAlmostEqual(r["sinp_mwh"], 233691.9, places=1)
    def test_find_links(self):
        html = '<a href="https://www.eby.gov.py/datos-oficiales-sobre-generacion-de-yacyreta-en-julio/"></a>'
        links = extractor.find_generation_links(html)
        self.assertTrue(len(links) >= 1)
if __name__ == "__main__":
    unittest.main()
