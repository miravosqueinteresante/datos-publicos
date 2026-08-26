import unittest, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from publicar_sitio import ajustar_ruta_lab

class TestPublicar(unittest.TestCase):
    def test_lab_ref_raiz(self):
        html = 'href="../www/index.html" src="../www/css/style.css"'
        out = ajustar_ruta_lab(html)
        self.assertIn('href="../index.html"', out)
        self.assertIn('src="../css/style.css"', out)
        self.assertNotIn("../www/", out)
    def test_sin_www_no_cambia(self):
        self.assertEqual(ajustar_ruta_lab("src='app.js'"), "src='app.js'")

if __name__ == "__main__":
    unittest.main()