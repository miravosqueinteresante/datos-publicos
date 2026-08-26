import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import es_de_asuncion

class TestFiltrar(unittest.TestCase):
    def test_nombre_municipalidad(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asuncion"))
    def test_nombre_con_tilde(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asunción"))
    def test_no_es_otro_org(self):
        self.assertFalse(es_de_asuncion("Ministerio de Salud Pública"))
    def test_no_universidad(self):
        self.assertFalse(es_de_asuncion("Universidad Nacional de Asunción"))

if __name__ == "__main__":
    unittest.main()