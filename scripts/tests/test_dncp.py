import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import es_de_asuncion
from dncp_contrataciones import mapear_fila
from dncp_contrataciones import validar

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

class TestValidar(unittest.TestCase):
    def test_filas_validas(self):
        filas = [
            {"id": "a", "objeto": "ob", "monto": "150"},
            {"id": "b", "objeto": "ob2", "monto": "300"},
        ]
        errores = validar(filas)
        self.assertEqual(len(errores), 0)
    def test_detecta_id_vacio(self):
        filas = [{"id": "", "objeto": "ob"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_objeto_vacio(self):
        filas = [{"id": "a", "objeto": ""}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_monto_no_numerico(self):
        filas = [{"id": "a", "objeto": "ob", "monto": "ABC"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)

if __name__ == "__main__":
    unittest.main()