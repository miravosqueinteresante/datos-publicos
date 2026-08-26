import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import es_de_asuncion
from dncp_contrataciones import mapear_fila

class TestFiltrar(unittest.TestCase):
    def test_nombre_municipalidad(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asuncion"))
    def test_nombre_con_tilde(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asunción"))
    def test_no_es_otro_org(self):
        self.assertFalse(es_de_asuncion("Ministerio de Salud Pública"))
    def test_no_universidad(self):
        self.assertFalse(es_de_asuncion("Universidad Nacional de Asunción"))

class TestMapear(unittest.TestCase):
    def test_extrae_campos_clave(self):
        fila = {
            "compiledRelease/id": "ocds-03ad3f-999",
            "compiledRelease/tender/title": "Construcción de vereda",
            "compiledRelease/tender/status": "active",
            "compiledRelease/buyer/name": "Municipalidad de Asuncion",
            "compiledRelease/tender/value/amount": "150000000",
            "compiledRelease/tender/value/currency": "PYG",
        }
        salida = mapear_fila(fila, {}, {}, {})
        self.assertEqual(salida["id"], "ocds-03ad3f-999")
        self.assertEqual(salida["objeto"], "Construcción de vereda")
        self.assertEqual(salida["monto"], "150000000")
    def test_campos_faltantes_quedan_vacios(self):
        salida = mapear_fila({"compiledRelease/id": "x"}, {}, {}, {})
        self.assertEqual(salida["objeto"], "")

if __name__ == "__main__":
    unittest.main()