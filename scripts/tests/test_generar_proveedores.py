import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_proveedores import calcular_top, es_directo

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,o1,,Bienes,Licitación Pública Nacional,Muni,P1,100,PYG,2024-01-01,,,x
b,o2,,Bienes,Menor cuantía nacional,Muni,P1,50,PYG,2024-02-01,,,x
c,o3,,Servicios,Licitación Pública Nacional,Muni,P2,300,PYG,2024-03-01,,,x
d,o4,,Obras,Contratación Directa,Muni,P2,200,PYG,2024-04-01,,,x
"""

class TestProveedores(unittest.TestCase):
    def test_es_directo(self):
        self.assertTrue(es_directo("Menor cuantía nacional"))
        self.assertTrue(es_directo("Contratación Directa"))
        self.assertTrue(es_directo("Contratación por Excepción"))
        self.assertFalse(es_directo("Licitación Pública Nacional"))
    def test_calcular_top_agrega_y_rankea(self):
        top = calcular_top(CSV)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["proveedor"], "P2")
        self.assertEqual(top[0]["monto_total"], 500)
        self.assertEqual(top[0]["contratos"], 2)
        self.assertEqual(top[1]["proveedor"], "P1")
        self.assertEqual(top[1]["monto_total"], 150)

if __name__ == "__main__":
    unittest.main()