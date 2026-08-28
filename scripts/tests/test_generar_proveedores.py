import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_proveedores import calcular_top, es_directo, categoria_es

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,valor_estimado,monto_adjudicado,monto_contratado,moneda,n_adjudicaciones,n_proveedores,proveedor,proveedores,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,o1,,goods,Licitación Pública Nacional,Muni,100,100,,PYG,1,1,P1,P1,2024-01-01,,,x
b,o2,,goods,Menor cuantía nacional,Muni,50,50,,PYG,1,1,P1,P1,2024-02-01,,,x
c,o3,,services,Licitación Pública Nacional,Muni,300,300,,PYG,1,1,P2,P2,2024-03-01,,,x
d,o4,,works,Contratación Directa,Muni,200,200,,PYG,1,1,P2,P2,2024-04-01,,,x
"""

class TestProveedores(unittest.TestCase):
    def test_es_directo(self):
        self.assertTrue(es_directo("Menor cuantía nacional"))
        self.assertTrue(es_directo("Contratación Directa"))
        self.assertTrue(es_directo("Contratación por Excepción"))
        self.assertFalse(es_directo("Licitación Pública Nacional"))
    def test_categoria_es_traduce(self):
        self.assertEqual(categoria_es("goods"), "Bienes")
        self.assertEqual(categoria_es("services"), "Servicios")
        self.assertEqual(categoria_es("works"), "Obras")
        self.assertEqual(categoria_es(""), "")
    def test_calcular_top_agrega_y_rankea(self):
        top = calcular_top(CSV)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["proveedor"], "P2")
        self.assertEqual(top[0]["monto_total"], 500)
        self.assertEqual(top[0]["adjudicaciones"], 2)
        self.assertEqual(top[1]["proveedor"], "P1")
        self.assertEqual(top[1]["monto_total"], 150)
        self.assertEqual(top[1]["categoria_principal"], "Bienes")
        self.assertEqual(top[0]["categoria_principal"], "Servicios")
        total_adj = top[0]["monto_total"] + top[1]["monto_total"]
        self.assertAlmostEqual(top[0]["pct_del_adjudicado"], top[0]["monto_total"]/total_adj*100, places=1)

if __name__ == "__main__":
    unittest.main()